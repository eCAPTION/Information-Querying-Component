from knowledge_graph.abstract_knowledge_graph import AbstractKnowledgeGraph
from utils.types import *
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from typing import Union

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
        kg_collection, properties_collection = self.__get_knowledge_graph_collection()
        self.kg_collection = kg_collection
        self.properties_collection = properties_collection

    def get_nodeids_with_name_containing(self, label_name: str) -> list[NodeID]:
        """
        Since we performed named entity linking in the NLP component, `label_name` would
        be the entityid itself.
        The original NewsLink paper used exact string matching to get the starting nodes for `label_name` here.
        """
        results = self.kg_collection.find({"q": label_name})
        return list(map(lambda r: int(r["q"]), results))

    def get_neighbors(self, entity_id: NodeID) -> list[tuple[NodeID, PropertyID]]:
        """
        Get neighboring nodeids for `entity_id`.
        """
        result = self.kg_collection.find_one({"q": entity_id}, {"n": True})

        if result == None:
            return []

        return list(map(lambda r: (int(r["e"]), int(r["p"])), result["n"]))

    def get_label_from_id(self, entity_id: NodeID) -> Union[Label, None]:
        document = self.kg_collection.find_one({"q": entity_id}, {"l": True})
        if document:
            return document["l"]
        else:
            return None

    def get_property_from_id(self, property_id: PropertyID) -> Union[Label, None]:
        document = self.properties_collection.find_one({"p": property_id}, {"l": True})
        if document:
            return document["l"]
        else:
            return None

    def __get_knowledge_graph_collection(self):
        uri = os.environ.get("MONGODB_URI")
        port = int(os.environ.get("MONGODB_PORT"))
        database = os.environ.get("MONGODB_DATABASE_NAME")
        kg_collection = os.environ.get("MONGODB_KNOWLEDGE_GRAPH_COLLECTION")
        properties_collection = os.environ.get("MONGODB_PROPERTIES_COLLECTION")

        client = MongoClient(uri, port)
        db_client = client[database]
        return (db_client[kg_collection], db_client[properties_collection])
