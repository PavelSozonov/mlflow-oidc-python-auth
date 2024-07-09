FROM python:3.8

WORKDIR /app

RUN apt-get update && apt-get install -y tcpdump && pip install mlflow==2.14.2

COPY client.py /app/client.py

COPY entrypoint.sh /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
