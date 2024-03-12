FROM python:3.9-slim

RUN mkdir -p /app
WORKDIR /app
COPY ./nlp .

RUN pip3 install -r requirements.txt

CMD ["sh", "-c", "exec faust -A main worker"]
