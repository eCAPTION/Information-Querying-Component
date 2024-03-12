from ecaption_utils.kafka.faust import (
    get_faust_app,
    initialize_topics,
    FaustApplication,
)
from ecaption_utils.kafka.topics import Topic, get_event_type
from utils import get_maximal_entity_cooccurrence_set
import os
from dotenv import load_dotenv

load_dotenv()

broker_url = os.environ.get("KAFKA_BROKER_URL")
port = os.environ.get("NLP_SERVICE_PORT")


app = get_faust_app(FaustApplication.NLP, broker_url=broker_url, port=port)
topics = initialize_topics(
    app,
    [Topic.NEW_ARTICLE_EXTRACTED, Topic.MAXIMAL_ENTITY_COOCCURRENCE_SET],
)


@app.agent(topics[Topic.NEW_ARTICLE_EXTRACTED])
async def handle_article_text(event_stream):
    async for event in event_stream:
        maximal_entity_cooccurrence_set = get_maximal_entity_cooccurrence_set(
            event.text
        )

        publish_to = Topic.MAXIMAL_ENTITY_COOCCURRENCE_SET
        Event = get_event_type(publish_to)
        event = Event(
            request_id=event.request_id,
            url=event.url,
            maximal_entity_cooccurrence_set=maximal_entity_cooccurrence_set,
        )

        await topics[publish_to].send(value=event)
