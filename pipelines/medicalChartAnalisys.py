from typing import List, Union, Generator, Iterator
import os
import asyncio
import httpx
import re

class Pipeline:
    def __init__(self):
        self.name = "Analisar Prontuários Médicos (+ Exames)"
        self.ollama_base_url = "http://ollama:11434"
        
        # ============================================
        # CONFIGURAÇÃO DA API
        # ============================================
        self.api_config = {
            "base_url": "http://host.docker.internal:3000",
            "endpoint_anamnese": "/api/v1/anamnese",
            "endpoint_arquivos": "/api/v1/arquivos",  # <--- NOVO ENDPOINT ADICIONADO
            "timeout": 30.0
        }
        
        print(f"__init__: {self.name} inicializado.")
        print(f"🔗 API configurada: {self.api_config['base_url']}")

    async def on_startup(self):
        """Verifica conexão com a API na inicialização"""
        print(f"on_startup: {self.name} - Verificando conexão com a API...")
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Testa endpoint de anamnese como healthcheck básico
                url = f"{self.api_config['base_url']}{self.api_config['endpoint_anamnese']}/"
                response = await client.get(url, params={"page": 1, "limit": 1})
                if response.status_code == 200:
                    print(f"✅ API conectada com sucesso!")
                else:
                    print(f"⚠️  API respondeu com status {response.status_code}")
        except Exception as e:
            print(f"⚠️  Aviso ao verificar API: {e}")

    async def on_shutdown(self):
        print("on_shutdown: Pipeline finalizado.")

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        """Processa a requisição do usuário"""
        
        anamnese_id = self._extrair_id_anamnese(user_message)
        id_especialidade = self._extrair_id_especialidade(user_message)
        
        if not anamnese_id:
            return "❌ Por favor, informe o ID da anamnese ou do paciente para iniciar a análise."

        try:
            # 1. BUSCA A ANAMNESE (Dados Subjetivos)
            anamnese = self._buscar_anamnese(anamnese_id, id_especialidade)
            
            if not anamnese:
                return f"❌ Anamnese/Paciente {anamnese_id} não encontrado(a)."

            # 2. IDENTIFICA O PACIENTE
            # O ID do paciente é necessário para buscar os arquivos
            id_paciente_real = anamnese.get('id_paciente')
            arquivos_exames = []

            if id_paciente_real:
                print(f"📂 Buscando exames para o paciente ID: {id_paciente_real}...")
                
                # 3. BUSCA OS ARQUIVOS/LAUDOS (Dados Objetivos)
                # <--- NOVA CHAMADA AQUI
                arquivos_exames = self._buscar_arquivos_paciente(str(id_paciente_real))
            else:
                print("⚠️ ID do paciente não encontrado na anamnese. Pulando busca de arquivos.")

            print(f"✅ Gerando análise para Anamnese {anamnese_id} com {len(arquivos_exames)} exames anexados.")

            # 4. GERA A ANÁLISE COMPLETA
            return self._gerar_analise_medica(anamnese, arquivos_exames, model_id)
                
        except Exception as e:
            print(f"🔴 Erro no pipeline: {e}")
            import traceback
            traceback.print_exc()
            return f"❌ **Erro interno:** {str(e)}"

    # ------------------------------------------------------------------
    # NOVOS MÉTODOS E MÉTODOS ATUALIZADOS
    # ------------------------------------------------------------------

    def _buscar_arquivos_paciente(self, id_paciente: str) -> List[dict]:
        """
        Busca arquivos na API filtrando pelo ID do paciente.
        Retorna apenas arquivos que tenham descrição (laudo).
        """
        try:
            url = f"{self.api_config['base_url']}{self.api_config['endpoint_arquivos']}"
            params = {"id_paciente": id_paciente}
            
            response = httpx.get(url, params=params, timeout=self.api_config['timeout'])
            
            if response.status_code == 200:
                data = response.json()
                # Garante que pegamos a lista correta independente do formato de resposta (envelope 'data' ou lista direta)
                lista_arquivos = data if isinstance(data, list) else data.get('data', [])
                
                # Filtra apenas arquivos que têm o campo 'descricao' preenchido
                # Isso evita enviar imagens sem laudo ou documentos administrativos vazios
                arquivos_com_laudo = [
                    arq for arq in lista_arquivos 
                    if arq.get('descricao') and str(arq.get('descricao')).strip()
                ]
                
                print(f"📄 Arquivos encontrados: {len(lista_arquivos)} | Com laudo útil: {len(arquivos_com_laudo)}")
                return arquivos_com_laudo
            
            elif response.status_code == 404:
                print("ℹ️ Nenhum arquivo encontrado para este paciente.")
                return []
            else:
                print(f"⚠️ Erro ao buscar arquivos: Status {response.status_code}")
                return []
                
        except Exception as e:
            print(f"🔴 Erro na requisição de arquivos: {e}")
            return []

    def _formatar_dados_completo(self, anamnese: dict, arquivos: List[dict]) -> str:
        """
        Formata tanto a Anamnese quanto os Arquivos para o Prompt da IA.
        """
        # --- Formatação da Anamnese (Código Base Anterior) ---
        paciente = anamnese.get('paciente', {})
        id_anamnese = anamnese.get('id_anamnese') or anamnese.get('id', 'N/A')
        
        texto_anamnese = f"""**DADOS DO PACIENTE:**
• **Nome:** {paciente.get('nome_completo', 'N/A') if paciente else 'N/A'}
• **Idade/Nasc:** {paciente.get('data_nascimento', 'N/A') if paciente else 'N/A'}

**DADOS CLÍNICOS (ANAMNESE):**
"""
        campos_ignorar = ['id', 'id_anamnese', 'id_paciente', 'id_especialidade', 'paciente', 'created_at', 'updated_at', 'descricao']
        
        # Se houver descrição na anamnese (queixa principal), colocamos em destaque
        if anamnese.get('descricao'):
             texto_anamnese += f"• **Queixa Principal / Descrição:** {anamnese.get('descricao')}\n"

        for chave, valor in anamnese.items():
            if chave not in campos_ignorar and valor not in [None, "", "null"]:
                chave_fmt = chave.replace('_', ' ').title()
                texto_anamnese += f"• **{chave_fmt}:** {valor}\n"

        # --- Formatação dos Arquivos (NOVA LÓGICA) ---
        texto_arquivos = "\n**LAUDOS E EXAMES COMPLEMENTARES ANEXADOS:**\n"
        
        if arquivos:
            for i, arq in enumerate(arquivos, 1):
                tipo = arq.get('tipo', 'Exame/Arquivo').upper()
                data_upload = arq.get('created_at', '')[:10] # Data YYYY-MM-DD
                descricao = arq.get('descricao', '').strip()
                
                texto_arquivos += f"""
--- EXAME {i}: {tipo} (Data: {data_upload}) ---
{descricao}
"""
        else:
            texto_arquivos += "(Nenhum exame ou laudo complementar encontrado no sistema)\n"

        return texto_anamnese + "\n" + texto_arquivos

    def _gerar_analise_medica(self, anamnese: dict, arquivos: List[dict], model_id: str) -> str:
        """Gera análise médica usando o modelo de IA com dados completos"""
        
        # Usa a nova função de formatação
        dados_completos = self._formatar_dados_completo(anamnese, arquivos)
        
        prompt = f"""Você é um assistente médico especializado. Analise o caso clínico abaixo combinando a anamnese com os resultados dos exames de imagem/laboratoriais anexados.

{dados_completos}

**SOLICITAÇÃO DE ANÁLISE:**
1.  **Resumo do Caso:** Sintetize o quadro clínico.
2.  **Correlação Clínica:** Relacione as queixas da anamnese com os achados nos laudos dos exames (ex: A ultrassonografia confirma a suspeita clínica?).
3.  **Achados Críticos:** Destaque qualquer alteração importante nos exames (ex: cistos, espessamento endometrial, etc).
4.  **Hipóteses Diagnósticas:** Baseado na soma de Anamnese + Exames.
5.  **Recomendações:** Sugira a conduta apropriada.

Responda de forma estruturada e profissional."""
        
        return self._call_ollama(prompt, model_id)

    # ------------------------------------------------------------------
    # MÉTODOS AUXILIARES (Mantidos do original)
    # ------------------------------------------------------------------

    def _buscar_anamnese(self, anamnese_id: str, id_especialidade: str = "1") -> dict:
        """Busca anamnese pelo ID do paciente (adaptado do seu código original)"""
        try:
            # Atenção: Ajuste a URL se necessário, mantive a lógica do seu código anterior
            url = f"{self.api_config['base_url']}{self.api_config['endpoint_anamnese']}/"
            
            # Buscamos listas e filtramos localmente para garantir match exato, 
            # ou passamos params se a API suportar filtro por query string
            params = {"page": 1, "limit": 100} 
            
            response = httpx.get(url, params=params, timeout=self.api_config['timeout'])

            if response.status_code == 200:
                data = response.json()
                anamneses = data if isinstance(data, list) else data.get('data', [])
                
                # Filtra pelo ID do paciente
                for a in anamneses:
                    # Converte para string para comparação segura
                    p_id = str(a.get('id_paciente', ''))
                    e_id = str(a.get('id_especialidade', ''))
                    
                    if p_id == str(anamnese_id) and e_id == str(id_especialidade):
                        return a
                return None
            return None
        except Exception as e:
            print(f"🔴 Erro ao buscar anamnese: {e}")
            return None

    def _call_ollama(self, user_prompt: str, model_id: str) -> str:
        """Chama o serviço Ollama"""
        system_prompt = "Você é um assistente médico especialista. Responda com precisão técnica baseada nos dados fornecidos."
        
        ollama_payload = {
            "model": "medgemma", # Forçando medgemma ou use model_id
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            # Aumentei o num_ctx pois agora temos textos de laudos que podem ser longos
            "options": {"temperature": 0.2, "num_ctx": 4096} 
        }

        try:
            response = httpx.post(
                f"{self.ollama_base_url}/api/chat",
                json=ollama_payload,
                timeout=120.0
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
        except Exception as e:
            return f"Erro ao conectar com Ollama: {str(e)}"

    def _extrair_id_anamnese(self, mensagem: str) -> str:
        # Mantido do seu código original
        match = re.search(r'(\d+)', mensagem)
        return match.group(1) if match else ""

    def _extrair_id_especialidade(self, mensagem: str) -> str:
        # Mantido do seu código original (padrão 1)
        return "1"