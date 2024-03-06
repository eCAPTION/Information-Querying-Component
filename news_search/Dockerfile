FROM python:3.9-slim

RUN mkdir -p /app
WORKDIR /app
COPY ./news_search .

RUN pip3 install -r requirements.txt

CMD ["sh", "-c", "python -m scripts.opensearch_setup && faust -A main worker"]
