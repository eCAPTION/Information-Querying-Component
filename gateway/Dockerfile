FROM python:3.9-slim

RUN mkdir -p /app
WORKDIR /app
COPY ./gateway .

RUN pip3 install -r requirements.txt

CMD ["sh", "-c", "exec uvicorn main:app --port $HTTP_GATEWAY_PORT --host 0.0.0.0"]
