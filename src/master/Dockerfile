FROM python:3.11

RUN apt update && apt install libpq-dev -y

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8080
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0"]
