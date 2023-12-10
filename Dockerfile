FROM python:3.9-slim

WORKDIR /app

COPY chat.py .
COPY vetorclock.py .
#COPY criptografia.py .
#COPY requirements.txt .

#RUN pip install --no-cache-dir -r requirements.txt

#EXPOSE 12345

CMD ["python", "./chat.py"]
#docker build -t chat .
#docker run -it chat
