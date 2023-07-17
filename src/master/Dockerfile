FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080
#ENTRYPOINT ["python", "./server.py"]
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0"]
