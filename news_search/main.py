from ecaption_utils.kafka.faust import (
    get_faust_app,
    initialize_topics,
    FaustApplication,
)
from ecaption_utils.kafka.topics import Topic, get_event_type
from utils.opensearch_client import OpenSearchClient
import os

broker_url = os.environ.get("KAFKA_BROKER_URL")
port = os.environ.get("NEWS_SEARCH_SERVICE")


app = get_faust_app(FaustApplication.NewsSearch, broker_url=broker_url, port=port)
topics = initialize_topics(
    app,
    [Topic.NEW_ARTICLE_EXTRACTED, Topic.NEWS_EMBEDDING, Topic.NEWS_SEARCH_RESULTS],
)

client = OpenSearchClient()


@app.agent(topics[Topic.NEWS_EMBEDDING])
async def handle_embedding(event_stream):
    """
    Given the news embedding corresponding to a news article URL,
    upserts the corresponding document embedding within the OpenSearch index.
    """
    async for event in event_stream:
        news_embedding_format = client.get_news_search_embedding_format(
            event.node_occurrences
        )
        document = client.upsert_document_with_url(
            event.url, {"embedding": news_embedding_format}
        )
        hits = client.search_similar_documents(
            text=document["text"],
            embedding=document["embedding"],
            beta=0.2,
        )

        related_articles = [
            {
                "url": hit["_source"]["url"],
                "title": hit["_source"]["title"],
                "image": hit["_source"]["image"],
                "description": hit["_source"]["description"],
                "similarity": hit["_score"],
            }
            for hit in hits
            if hit["_source"]["url"] != event.url
        ]

        publish_to = Topic.NEWS_SEARCH_RESULTS
        Event = get_event_type(publish_to)
        event = Event(
            request_id=event.request_id,
            url=event.url,
            title=document["title"],
            image=document["image"],
            description=document["description"],
            related_articles=related_articles,
            adjlist=event.adjlist,
            node_occurrences=event.node_occurrences,
            entity_labels=event.entity_labels,
            property_labels=event.property_labels,
        )

        await topics[publish_to].send(value=event)


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
