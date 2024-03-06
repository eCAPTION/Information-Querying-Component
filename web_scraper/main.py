from ecaption_utils.kafka.faust import (
    get_faust_app,
    initialize_topics,
    FaustApplication,
)
from ecaption_utils.kafka.topics import Topic, get_event_type
from utils import extract_article_url
import os

broker_url = os.environ.get("KAFKA_BROKER_URL")
port = os.environ.get("WEB_SCRAPER_SERVICE_PORT")

app = get_faust_app(FaustApplication.WebScraper, broker_url=broker_url, port=port)
topics = initialize_topics(
    app,
    [
        Topic.NEW_ARTICLE_URL,
        Topic.NEW_ARTICLE_EXTRACTED,
    ],
)


@app.agent(topics[Topic.NEW_ARTICLE_URL])
async def handle_new_article(event_stream):
    async for event in event_stream:
        extracted = extract_article_url(event.url)

        publish_to = Topic.NEW_ARTICLE_EXTRACTED
        Event = get_event_type(publish_to)
        event = Event(
            request_id=event.request_id,
            url=event.url,
            title=extracted.get("title"),
            description=extracted.get("description"),
            text=extracted.get("text"),
            image=extracted.get("image"),
        )

        await topics[publish_to].send(value=event)
