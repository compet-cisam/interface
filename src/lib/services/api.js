// @ts-nocheck

const BASE_URL = 'http://localhost:3000'; 

export async function buscarDados(endpoint) {
    try {
        const resposta = await fetch(`${BASE_URL}${endpoint}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!resposta.ok) {
            throw new Error(`Erro na requisição: ${resposta.status}`);
        }

        return await resposta.json();
    } catch (erro) {
        console.error("Erro ao buscar dados:", erro);
        throw erro;
    }
}

export async function enviarDados(endpoint, corpoDosDados) {
    try {
        const resposta = await fetch(`${BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(corpoDosDados)
        });

        const dadosResposta = await resposta.json();

        if (!resposta.ok) {
            const mensagemErro = dadosResposta.detail || 'Erro ao enviar dados';
            throw new Error(mensagemErro);
        }

        return dadosResposta;

    } catch (erro) {
        console.error("Erro ao enviar dados:", erro);
        throw erro;
    }
}