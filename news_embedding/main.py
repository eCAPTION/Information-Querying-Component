from ecaption_utils.kafka.faust import (
    get_faust_app,
    initialize_topics,
    FaustApplication,
)
from ecaption_utils.kafka.topics import Topic, get_event_type
from g_star_search import GStarSearch
from knowledge_graph.mongo_knowledge_graph import MongoKnowledgeGraph
from utils.types import *
import os

broker_url = os.environ.get("KAFKA_BROKER_URL")
port = os.environ.get("NEWS_EMBEDDING_SERVICE")


app = get_faust_app(FaustApplication.NewsEmbedding, broker_url=broker_url, port=port)
topics = initialize_topics(
    app,
    [Topic.MAXIMAL_ENTITY_COOCCURRENCE_SET, Topic.NEWS_EMBEDDING],
)


@app.agent(topics[Topic.MAXIMAL_ENTITY_COOCCURRENCE_SET])
async def generate_embedding(event_stream):
    kg = MongoKnowledgeGraph()
    gstar = GStarSearch(kg)

    async for event in event_stream:
        node_occurrences: dict[NodeID, int] = {}
        combined_adjlist: Embedding_Adjlist = {}

        for label_set in event.maximal_entity_cooccurrence_set:
            adjlist = gstar.get_lcag(label_set)

            for node, neighbors in adjlist.items():
                if not node_occurrences.get(node):
                    node_occurrences[node] = 0
                if not combined_adjlist.get(node):
                    combined_adjlist[node] = set()

                node_occurrences[node] += 1
                combined_adjlist[node].update(neighbors)

        for key in combined_adjlist.keys():
            combined_adjlist[key] = list(combined_adjlist[key])

        publish_to = Topic.NEWS_EMBEDDING
        Event = get_event_type(publish_to)
        event = Event(
            request_id=event.request_id,
            url=event.url,
            adjlist=combined_adjlist,
            node_occurrences=node_occurrences,
        )

        await topics[publish_to].send(value=event)
