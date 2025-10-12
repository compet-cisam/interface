from typing import List, Union, Generator, Iterator
import os
import asyncio
import httpx
import re

class Pipeline:
    def __init__(self):
        self.name = "Analisar Prontuários Médicos"
        self.ollama_base_url = "http://ollama:11434"
        
        # ============================================
        # CONFIGURAÇÃO DA API
        # ============================================
        self.api_config = {
            "base_url": "http://host.docker.internal:3000",
            "endpoint": "/api/v1/anamnese",
            "timeout": 30.0
        }
        
        print(f"__init__: {self.name} inicializado.")
        print(f"🔗 API configurada: {self.api_config['base_url']}{self.api_config['endpoint']}")

    async def on_startup(self):
        """Verifica conexão com a API na inicialização"""
        print(f"on_startup: {self.name} - Verificando conexão com a API...")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                url = f"{self.api_config['base_url']}{self.api_config['endpoint']}/"
                response = await client.get(
                    url,
                    params={"page": 1, "limit": 1}
                )
                
                if response.status_code == 200:
                    print(f"✅ API conectada com sucesso!")
                    data = response.json()
                    print(f"📊 API respondeu corretamente")
                else:
                    print(f"⚠️  API respondeu com status {response.status_code}")
                    
        except httpx.ConnectError:
            print(f"🔴 Erro: Não foi possível conectar à API em {self.api_config['base_url']}")
            print("💡 Verifique se o serviço está rodando e se host.docker.internal está acessível")
        except Exception as e:
            print(f"⚠️  Aviso ao verificar API: {e}")

    async def on_shutdown(self):
        print("on_shutdown: Pipeline finalizado.")

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        """Processa a requisição do usuário"""
        
        # Extrai o ID da anamnese da mensagem
        anamnese_id = self._extrair_id_anamnese(user_message)
        
        if not anamnese_id:
            return """📋 **Sistema de Análise de Prontuários Médicos**

Para consultar um paciente, digite o **ID da anamnese**:

**Exemplos:**
• "Analisar anamnese 123"
• "Buscar prontuário 456"
• "Consultar paciente 789"
• Ou simplesmente: "123"

💡 O sistema buscará a anamnese na base de dados e gerará uma análise médica completa."""

        try:
            # Busca a anamnese pelo ID
            anamnese = self._buscar_anamnese_por_id(anamnese_id)
            
            if not anamnese:
                return f"""❌ **Anamnese não encontrada**

A anamnese com ID '{anamnese_id}' não foi localizada no sistema.

💡 **Dicas:**
• Verifique se o ID está correto
• Confirme se a anamnese existe na base de dados
• Tente listar as anamneses disponíveis primeiro"""

            print(f"✅ Anamnese ID {anamnese_id} encontrada. Gerando análise...")

            return self._gerar_analise_medica(anamnese, model_id)
                
        except Exception as e:
            print(f"🔴 Erro no pipeline: {e}")
            import traceback
            traceback.print_exc()
            return f"❌ **Erro interno:** {str(e)}"

    def _extrair_id_anamnese(self, mensagem: str) -> str:
        """Extrai o ID da anamnese da mensagem do usuário"""
        mensagem = mensagem.strip()
        
        # Padrões para capturar o ID
        padroes = [
            r'anamnese\s+(\d+)',
            r'prontuário\s+(\d+)',
            r'consultar\s+(?:paciente\s+)?(\d+)',
            r'buscar\s+(?:paciente\s+)?(\d+)',
            r'analisar\s+(?:paciente\s+)?(\d+)',
            r'paciente\s+(\d+)',
            r'id\s+(\d+)',
            r'^(\d+)$',  # Apenas números
        ]
        
        for padrao in padroes:
            match = re.search(padrao, mensagem, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ""

    def _buscar_anamnese_por_id(self, anamnese_id: str) -> dict:
        """Busca anamnese pelo ID via API REST"""
        try:
            # Monta a URL com o ID
            url = f"{self.api_config['base_url']}{self.api_config['endpoint']}/{anamnese_id}"
            
            print(f"🔍 Buscando anamnese ID '{anamnese_id}'...")
            print(f"🌐 URL: {url}")
            
            response = httpx.get(
                url,
                timeout=self.api_config['timeout']
            )
            
            print(f"📡 Status da resposta: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Anamnese encontrada!")
                return data
                    
            elif response.status_code == 404:
                print(f"❌ Anamnese ID {anamnese_id} não encontrada")
                return None
            else:
                print(f"🔴 API retornou status {response.status_code}")
                print(f"📄 Resposta: {response.text[:200]}")
                return None
                
        except httpx.TimeoutException:
            print(f"🔴 Timeout ao buscar na API (>{self.api_config['timeout']}s)")
            return None
        except httpx.ConnectError as e:
            print(f"🔴 Erro de conexão com a API: {self.api_config['base_url']}")
            print(f"💡 Verifique se o serviço está rodando e se host.docker.internal está configurado")
            print(f"🔧 Erro: {e}")
            return None
        except Exception as e:
            print(f"🔴 Erro ao buscar na API: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _gerar_analise_medica(self, anamnese: dict, model_id: str) -> str:
        """Gera análise médica usando o modelo de IA"""
        
        dados_formatados = self._formatar_dados_anamnese(anamnese)
        
        prompt = f"""Você é um assistente médico especializado em análise de prontuários ginecológicos. Analise as informações da anamnese abaixo e forneça uma avaliação médica estruturada.

{dados_formatados}

**SOLICITAÇÃO:**
Forneça uma análise médica estruturada seguindo este formato:

## 📋 RESUMO CLÍNICO
[Breve resumo da condição atual do paciente baseado nos dados da anamnese - máximo 3-4 linhas]

## 🔍 PRINCIPAIS ACHADOS
[Liste os pontos mais relevantes do histórico médico, queixas atuais e dados da anamnese]

## 💊 RECOMENDAÇÕES
[Sugestões de acompanhamento, exames complementares ou cuidados preventivos baseados nos dados coletados]

## ⚠️ PONTOS DE ATENÇÃO
[Fatores que requerem monitoramento especial, sinais de alerta ou que apresentam maior risco]

## 🩺 CONSIDERAÇÕES FINAIS
[Avaliação geral e necessidade de procedimentos adicionais baseado nas informações da anamnese]

**NOTAS IMPORTANTES:**
- HD = Histeroscopia Diagnóstica
- MAC = Método Anticoncepcional
- G/P/A = Gestações/Partos/Abortos
- Esta é uma análise informativa baseada em IA
- Sempre consulte um profissional de saúde qualificado para decisões médicas definitivas"""
        
        return self._call_ollama(prompt, model_id)

    def _formatar_dados_anamnese(self, anamnese: dict) -> str:
        """Formata os dados da anamnese para o prompt"""
        
        # Função auxiliar para formatar valores
        def fmt(valor, padrao="Não informado"):
            return valor if valor not in [None, "", "null"] else padrao
        
        # Extrai informações do paciente (se estiver no objeto anamnese)
        paciente = anamnese.get('paciente', {})
        
        resultado = f"""**DADOS DO PACIENTE:**
• **ID da Anamnese:** {anamnese.get('id', 'N/A')}
• **Nome do Paciente:** {paciente.get('nome_completo', 'N/A') if paciente else 'N/A'}
• **Data de Nascimento:** {paciente.get('data_nascimento', 'N/A') if paciente else 'N/A'}

**DADOS DA ANAMNESE:**
"""
        
        # Adiciona todos os campos da anamnese dinamicamente
        campos_ignorar = ['id', 'paciente', 'created_at', 'updated_at', 'paciente_id']
        
        for chave, valor in anamnese.items():
            if chave not in campos_ignorar and valor not in [None, "", "null"]:
                # Formata a chave (transforma snake_case em Título)
                chave_formatada = chave.replace('_', ' ').title()
                resultado += f"• **{chave_formatada}:** {valor}\n"
        
        # Se não houver dados além dos básicos
        if len([k for k in anamnese.keys() if k not in campos_ignorar]) == 0:
            resultado += "• Nenhum dado adicional de anamnese registrado\n"
        
        return resultado

    def _call_ollama(self, user_prompt: str, model_id: str) -> str:
        """Chama o serviço Ollama para gerar a análise"""
        
        system_prompt = """Você é um assistente médico especializado em análise de prontuários e anamneses ginecológicas. 
Forneça análises médicas estruturadas, precisas e baseadas em evidências científicas. 
Mantenha um tom profissional, empático e científico.
Sempre inclua avisos sobre a necessidade de consulta médica profissional.
Seja objetivo e direto nas recomendações.
Considere todos os dados fornecidos na anamnese para fazer uma avaliação completa."""

        print("--- PIPE: Enviando payload de chat para o Ollama ---")
        
        ollama_payload = {
            "model": 'medgemma', 
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9
            }
        }

        try:
            print("--- PIPE: Aguardando resposta do Ollama (timeout de 5 minutos)... ---")
            response = httpx.post(
                f"{self.ollama_base_url}/api/chat",
                json=ollama_payload,
                timeout=300.0
            )
            response.raise_for_status()
            response_data = response.json()
            
            if "message" in response_data and "content" in response_data["message"]:
                print("✅ Resposta recebida do Ollama com sucesso!")
                return response_data["message"]["content"].strip()
            else:
                print(f"🔴 Resposta inesperada do Ollama: {response_data}")
                return "Ollama não retornou uma mensagem com conteúdo válido."
                
        except httpx.RequestError as e:
            print(f"🔴 Erro de rede ao chamar Ollama: {e}")
            return "Erro de conexão com o serviço de análise."
        except httpx.HTTPStatusError as e:
            print(f"🔴 Erro HTTP do Ollama: {e.response.status_code} - {e.response.text}")
            return "Erro no serviço de análise (status HTTP)."
        except Exception as e:
            print(f"🔴 Erro inesperado ao chamar Ollama: {e}")
            return "Erro interno no serviço de análise."