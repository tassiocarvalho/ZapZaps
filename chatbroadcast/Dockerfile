#imagem base do Python
FROM python:3.8-slim

#diretório de trabalho
WORKDIR /app

#dependências
COPY requirements.txt .
#RUN pip install -r requirements.txt

# Copia os arquivos de código para o container
COPY . .

# Executar o chat.py quando o container iniciar
CMD ["python", "./chatv5.py"]


#docker build -t meu-chat .
#docker run --rm -it meu-chat