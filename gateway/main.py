from fastapi import FastAPI
from typing import Union
import asyncio
from ecaption_utils.kafka.faust import (
    get_faust_app,
    initialize_topics,
    FaustApplication,
)
from ecaption_utils.kafka.topics import Topic, get_event_type


async def lifespan(app: FastAPI):
    """
    Defines the FastAPI lifespan events - i.e. additional startup and shutdown configurations.

    See: https://fastapi.tiangolo.com/advanced/events/
    """

    # On start up
    global topics

    faust_app = get_faust_app(FaustApplication.Gateway)
    topics = initialize_topics(faust_app, [Topic.NEW_ARTICLE_URL])

    # start the faust app in client mode
    asyncio.create_task(faust_app.start_client())

    yield

    # On shut down
    faust_app.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/relatedarticles")
async def related_articles(url: Union[str, None] = None):
    topic = Topic.NEW_ARTICLE_URL
    Event = get_event_type(topic)
    event = Event(url=url)

    await topics[topic].send(value=event)

    return "Sent: {}".format(event)
