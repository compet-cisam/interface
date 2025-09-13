#!/bin/bash

set -e

echo "Verificando arquivos e diretórios necessários..."
if [ ! -f ".example.env" ] && [ ! -f ".env" ]; then
    echo "Erro: Nenhum arquivo de ambiente (.example.env ou .env) encontrado!"
    exit 1
fi

if [ ! -d "modelfiles" ]; then
    echo "Diretório 'modelfiles' não encontrado. Criando..."
    mkdir modelfiles
fi

if [ -f ".example.env" ] && [ ! -f ".env" ]; then
    echo "Criando arquivo .env a partir de .example.env..."
    mv .example.env .env
else
    echo "Arquivo .env já existe. Pulando a criação."
fi

echo "Iniciando os contêineres do Ollama com Docker Compose..."
docker compose up -d

echo "Aguardando 10 segundos para o serviço Ollama inicializar..."
sleep 10

echo "Entrando no diretório do modelo..."
cd modelfiles/

MODEL_FILE="medgemma-4b-it-Q8_0.gguf"
MODELS_URL="https://huggingface.co/kelkalot/medgemma-4b-it-GGUF/resolve/main/${MODEL_FILE}"

if [ ! -f "$MODEL_FILE" ]; then
    echo "Baixando o modelo MedGemma... Isso pode demorar."
    wget -O "$MODEL_FILE" "$MODELS_URL"
else
    echo "O arquivo do modelo ${MODEL_FILE} já existe. Pulando o download."
fi

cd ..

MODL_FILE_PATH="./modelfiles/Modelfile.txt"

if [ ! -f "$MODL_FILE_PATH" ]; then
    echo "Erro: Arquivo Modelfile não encontrado em ${MODL_FILE_PATH}"
    exit 1
fi

echo "Copiando o modelo GGUF para dentro do contêiner ollama..."
docker cp "./modelfiles/${MODEL_FILE}" ollama:/${MODEL_FILE}

echo "Copiando o Modelfile para dentro do contêiner ollama..."
docker cp "$MODL_FILE_PATH" ollama:/modelfile.txt

echo "Criando o modelo medgemma no Ollama dentro do contêiner..."
docker exec -it ollama ollama create medgemma -f /modelfile.txt

echo "Limpando arquivos temporários de dentro do contêiner..."
docker exec ollama rm /${MODEL_FILE} /modelfile.txt

echo "Pronto! O modelo medgemma deve estar disponível no Ollama."