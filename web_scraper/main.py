from ecaption_utils.kafka.faust import (
    get_faust_app,
    initialize_topics,
    get_error_handler,
    FaustApplication,
)
from ecaption_utils.kafka.topics import Topic, get_event_type
from utils import extract_article_url, check_whitelist, is_https
import os
from urllib.parse import urlparse, urljoin

broker_url = os.environ.get("KAFKA_BROKER_URL")
port = os.environ.get("WEB_SCRAPER_SERVICE_PORT")

app = get_faust_app(FaustApplication.WebScraper, broker_url=broker_url, port=port)
topics = initialize_topics(
    app,
    [Topic.NEW_ARTICLE_URL, Topic.NEW_ARTICLE_EXTRACTED],
)
handle_error = get_error_handler(app)


@app.agent(topics[Topic.NEW_ARTICLE_URL])
async def handle_new_article(event_stream):
    async for event in event_stream:
        parsed_url = urlparse(event.url)

        if not is_https(parsed_url):
            await handle_error(
                event.request_id,
                error_type=FaustApplication.WebScraper,
                error_message=f"URL is not HTTPs! {event.url}",
            )
            continue
        if not check_whitelist(parsed_url):
            await handle_error(
                event.request_id,
                error_type=FaustApplication.WebScraper,
                error_message=f"URL not whitelisted! {event.url}",
            )
            continue

        stripped_url = urljoin(event.url, parsed_url.path)

        try:
            extracted = extract_article_url(stripped_url)
        except Exception as e:
            await handle_error(
                event.request_id,
                error_type=FaustApplication.WebScraper,
                error_message=str(e),
            )
            continue

        publish_to = Topic.NEW_ARTICLE_EXTRACTED
        Event = get_event_type(publish_to)
        event = Event(
            request_id=event.request_id,
            url=stripped_url,
            title=extracted.get("title"),
            description=extracted.get("description"),
            text=extracted.get("text"),
            image=extracted.get("image"),
        )

        await topics[publish_to].send(value=event)
