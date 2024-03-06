from ecaption_utils.kafka.faust import (
    get_faust_app,
    initialize_topics,
    FaustApplication,
)
from ecaption_utils.kafka.topics import Topic
from utils.opensearch_client import OpenSearchClient
import os

broker_url = os.environ.get("KAFKA_BROKER_URL")
port = os.environ.get("NEWS_SEARCH_SERVICE")


app = get_faust_app(FaustApplication.NewsSearch, broker_url=broker_url, port=port)
topics = initialize_topics(
    app,
    [Topic.NEW_ARTICLE_EXTRACTED],
)

client = OpenSearchClient()


@app.agent(topics[Topic.NEW_ARTICLE_EXTRACTED])
async def handle_new_article_extracted(event_stream):
    """
    Given the contents of a news article URL,
    upserts the corresponding document within the OpenSearch index.
    """
    async for event in event_stream:
        fields = {
            "title": event.title,
            "description": event.description,
            "text": event.text,
            "image": event.image,
        }
        client.upsert_document_with_url(event.url, fields=fields)
