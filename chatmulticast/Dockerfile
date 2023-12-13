# Imagem base do Python
FROM python:3.8-slim

# Diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos de código para o container
COPY . .

# Executar o chat.py quando o container iniciar
CMD ["python", "./multicastchat.py"]

#docker build -t meu-chat .
#docker run --rm -it meu-chat