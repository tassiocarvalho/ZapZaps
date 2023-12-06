# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o script Python para o diretório de trabalho no container
COPY chat.py .
COPY vetorclock.py .

# Informe ao Docker que a aplicação escuta na porta 12345
EXPOSE 12345

# Comando para executar o script Python quando o container iniciar
CMD ["python", "./chat.py"]

#docker build -t chat .
#docker run -it chat
