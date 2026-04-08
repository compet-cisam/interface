<script>
    import { buscarDados, enviarDados } from '$lib/services/api.js';

    let resultado = "Aguardando ação...";
    let carregando = false;
    let erro = false;

    // Função para testar o GET (Buscar dados)
    async function testarBusca() {
        carregando = true;
        erro = false;
        resultado = "Buscando...";

        try {
            // Tenta buscar na raiz da API ou um endpoint de saúde se houver
            // Se sua API não tiver a rota '/', troque por algo que exista, ex: '/users'
            const dados = await buscarDados('/'); 
            resultado = JSON.stringify(dados, null, 2); // Formata bonito
        } catch (e) {
            erro = true;
            resultado = "Erro ao buscar: " + e.message;
            console.error(e);
        } finally {
            carregando = false;
        }
    }

    // Função para testar o POST (Login simulado)
    async function testarLogin() {
        carregando = true;
        erro = false;
        resultado = "Enviando login...";

        const dadosLogin = {
            email: "teste@exemplo.com",
            password: "123"
        };

        try {
            // Tenta enviar para a rota de login (verifique se é /auth/login ou /token no seu backend)
            const resposta = await enviarDados('/auth/login', dadosLogin);
            resultado = JSON.stringify(resposta, null, 2);
        } catch (e) {
            erro = true;
            resultado = "Erro no login: " + e.message;
            console.error(e);
        } finally {
            carregando = false;
        }
    }
</script>

<div class="container">
    <h1>Teste de Integração API</h1>
    <p>Use os botões abaixo para testar a conexão com o backend rodando no Docker.</p>

    <div class="actions">
        <button on:click={testarBusca} disabled={carregando}>
            Testar GET (Busca)
        </button>

        <button on:click={testarLogin} disabled={carregando} class="secondary">
            Testar POST (Login)
        </button>
    </div>

    <div class="status {erro ? 'erro' : ''}">
        <h3>Resultado:</h3>
        <pre>{resultado}</pre>
    </div>
</div>

<style>
    .container {
        max-width: 600px;
        margin: 40px auto;
        font-family: sans-serif;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #f9f9f9;
    }

    h1 { color: #333; }

    .actions {
        display: flex;
        gap: 10px;
        margin: 20px 0;
    }

    button {
        padding: 10px 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
    }

    button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }

    button.secondary {
        background-color: #28a745;
    }

    .status {
        background: #fff;
        padding: 15px;
        border: 1px solid #eee;
        border-radius: 4px;
        min-height: 100px;
    }

    .status.erro {
        border-color: #ff0000;
        background-color: #fff0f0;
        color: #d8000c;
    }

    pre {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
</style>