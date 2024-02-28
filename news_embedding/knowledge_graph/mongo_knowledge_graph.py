from knowledge_graph.abstract_knowledge_graph import AbstractKnowledgeGraph
from utils.types import *
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()


class MongoKnowledgeGraph(AbstractKnowledgeGraph):
    """
    Each entry in MongoDB consists of:
    {
        q: <WIKIDATA_ENTITY_ID>,
        l: <WIKIDATA_LABEL>,
        n: [<WIKIDATA_ENTITY_ID>] # of neighboring entities
    }

    Refer to scripts/unzip.py for more information
    """

    def __init__(self) -> None:
        self.kg_collection = self.__get_knowledge_graph_collection()

    def get_nodeids_with_name_containing(self, label_name: str) -> list[NodeID]:
        """
        Since we performed named entity linking in the NLP component, `label_name` would
        be the entityid itself.
        The original NewsLink paper used exact string matching to get the starting nodes for `label_name` here.
        """
        results = self.kg_collection.find({"q": label_name})
        return list(map(lambda r: int(r["q"]), results))

    def get_neighbors(self, entity_id: NodeID) -> list[NodeID]:
        """
        Get neighboring nodeids for `entity_id`.
        """
        result = self.kg_collection.find_one({"q": entity_id}, {"n": True})

        if result == None:
            return []

        return list(map(lambda r: int(r), result["n"]))

    def __get_knowledge_graph_collection(self):
        uri = os.environ.get("MONGODB_URI")
        port = int(os.environ.get("MONGODB_PORT"))
        database = os.environ.get("MONGODB_DATABASE_NAME")
        collection = os.environ.get("MONGODB_KNOWLEDGE_GRAPH_COLLECTION")

        client = MongoClient(uri, port)
        return client[database][collection]
