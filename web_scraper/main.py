from ecaption_utils.kafka.faust import (
    get_faust_app,
    initialize_topics,
    FaustApplication,
)
from ecaption_utils.kafka.topics import Topic, get_event_type
from utils import get_text_from_article_url

app = get_faust_app(FaustApplication.WebScraper)
topics = initialize_topics(
    app,
    [
        Topic.NEW_ARTICLE_URL,
        Topic.NEW_ARTICLE_TEXT,
    ],
)


@app.agent(topics[Topic.NEW_ARTICLE_URL])
async def handle_new_article(event_stream):
    async for event in event_stream:
        article_text = get_text_from_article_url(event.url)

        publish_to = Topic.NEW_ARTICLE_TEXT
        Event = get_event_type(publish_to)
        event = Event(url=event.url, text=article_text)

        await topics[publish_to].send(value=event)
