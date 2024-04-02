from ecaption_utils.kafka.faust import (
    get_faust_app,
    initialize_topics,
    FaustApplication,
)
from ecaption_utils.kafka.topics import Topic, get_event_type
import os
from dotenv import load_dotenv

load_dotenv()

broker_url = os.environ.get("KAFKA_BROKER_URL")
port = os.environ.get("FACT_QUERYING_SERVICE")


app = get_faust_app(FaustApplication.FactQuerying, broker_url=broker_url, port=port)
topics = initialize_topics(
    app,
    [Topic.NEWS_SEARCH_RESULTS, Topic.INFORMATION_QUERYING_RESULTS],
)


@app.agent(topics[Topic.NEWS_SEARCH_RESULTS])
async def handle_news_search_results(event_stream):
    async for event in event_stream:
        related_facts_dict: dict[int, list[str]] = {}
        entity_labels = event.entity_labels
        property_labels = event.property_labels

        for node_id, neighbors in event.adjlist.items():
            if not related_facts_dict.get(node_id):
                related_facts_dict[node_id] = []

            for neighbor_id, property_id in neighbors:
                node_label = entity_labels.get(str(node_id))
                property_label = property_labels.get(str(property_id))
                neighbor_label = entity_labels.get(str(neighbor_id))

                fact = f"{neighbor_label} is {property_label} of {node_label}"
                related_facts_dict[node_id].append(fact)

        node_ids_in_decreasing_importance = [
            node_id
            for node_id, num_occurrences in sorted(event.node_occurrences.items(), key=lambda item: item[1], reverse=True)
        ]
        related_facts = [fact for node_id in node_ids_in_decreasing_importance for fact in related_facts_dict[node_id]]

        publish_to = Topic.INFORMATION_QUERYING_RESULTS
        Event = get_event_type(publish_to)
        event = Event(
            request_id=event.request_id,
            url=event.url,
            title=event.title,
            description=event.description,
            image=event.image,
            related_articles=event.related_articles,
            related_facts=related_facts,
            adjlist=event.adjlist,
            node_occurrences=event.node_occurrences,
            entity_labels=event.entity_labels,
            property_labels=event.property_labels,
        )

        await topics[publish_to].send(value=event)
