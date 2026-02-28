@echo off
setlocal enabledelayedexpansion

echo Verificando arquivos e diretorios necessarios...
if not exist ".example.env" if not exist ".env" (
    echo Erro: Nenhum arquivo de ambiente ^(.example.env ou .env^) encontrado!
    exit /b 1
)

if not exist "modelfiles" (
    echo Diretorio 'modelfiles' nao encontrado. Criando...
    mkdir modelfiles
)

if exist ".example.env" if not exist ".env" (
    echo Criando arquivo .env a partir de .example.env...
    move .example.env .env
) else (
    echo Arquivo .env ja existe. Pulando a criacao.
)

echo Iniciando os conteineres do Ollama com Docker Compose...
docker compose up -d

echo Aguardando 10 segundos para o servico Ollama inicializar...
timeout /t 10 /nobreak >nul

echo Entrando no diretorio do modelo...
cd modelfiles

set MODEL_FILE=medgemma-4b-it-Q8_0.gguf
set MODELS_URL=https://huggingface.co/kelkalot/medgemma-4b-it-GGUF/resolve/main/%MODEL_FILE%

if not exist "%MODEL_FILE%" (
    echo Baixando o modelo MedGemma... Isso pode demorar.
    curl -L -o "%MODEL_FILE%" "%MODELS_URL%"
    if errorlevel 1 (
        echo Erro ao baixar o modelo. Tentando com wget...
        wget -O "%MODEL_FILE%" "%MODELS_URL%"
        if errorlevel 1 (
            echo Erro: Falha no download do modelo. Verifique sua conexao.
            cd ..
            exit /b 1
        )
    )
) else (
    echo O arquivo do modelo %MODEL_FILE% ja existe. Pulando o download.
)

cd ..

set MODL_FILE_PATH=.\modelfiles\Modelfile.txt

if not exist "%MODL_FILE_PATH%" (
    echo Erro: Arquivo Modelfile nao encontrado em %MODL_FILE_PATH%
    exit /b 1
)

echo Copiando o modelo GGUF para dentro do conteiner ollama...
docker cp ".\modelfiles\%MODEL_FILE%" ollama:/%MODEL_FILE%

echo Copiando o Modelfile para dentro do conteiner ollama...
docker cp "%MODL_FILE_PATH%" ollama:/modelfile.txt

echo Criando o modelo medgemma no Ollama dentro do conteiner...
docker exec -it ollama ollama create medgemma -f /modelfile.txt

echo Limpando arquivos temporarios de dentro do conteiner...
docker exec ollama rm /%MODEL_FILE% /modelfile.txt

echo Pronto! O modelo medgemma deve estar disponivel no Ollama.

pause