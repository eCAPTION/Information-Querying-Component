from dotenv import load_dotenv
import os
from opensearchpy import OpenSearch

load_dotenv()


class OpenSearchClient:
    embedding_split_char = "<SPLIT>"
    index_name = "ns_component"

    def __init__(self) -> None:
        self.client = self.__get_opensearch_client()

    def upsert_document_with_url(self, url: str, fields: dict):
        """
        Indexes a new document with the given url and fields if there are no existing documents matching the provided url.
        If a matching document exists, performs an update query to update that document instead of creating a new one.
        """
        url_query = {"url": url}
        existing_documents = self.search_match_query(url_query)

        document = fields.copy()
        document["url"] = url

        if len(existing_documents):
            for existing_document in existing_documents:
                id = existing_document["_id"]
                self.client.update(
                    self.index_name, id, {"doc": document}, refresh="wait_for"
                )
        else:
            self.client.index(self.index_name, document, refresh="wait_for")

        updated_document = self.search_match_query(url_query)[0]
        return updated_document["_source"]

    def search_match_query(self, fields: dict):
        query = {"query": {"match": fields}}
        response = self.client.search(body=query, index=self.index_name)
        hits = response["hits"]["hits"]

        return hits

    def search_similar_documents(self, text: str, embedding: str, beta: float):
        """
        Searches for the top-k similar documents with the given text and embedding parameters
        by performing a weighted boolean query using OpenSearch's default BM25 implementation.
        `beta` controls the weight proportion allocated to the embedding similarity score vs the
        text similarity score. (i.e. weight of text similarity score = `1-beta`)
        """
        weighted_bool_query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "function_score": {
                                "query": {"match": {"embedding": embedding}},
                                "boost": beta,
                            }
                        },
                        {
                            "function_score": {
                                "query": {"match": {"text": text}},
                                "boost": 1 - beta,
                            }
                        },
                    ]
                }
            }
        }
        response = self.client.search(body=weighted_bool_query, index=self.index_name)
        hits = response["hits"]["hits"]
        return hits

    def get_news_search_embedding_format(self, node_occurrences: dict[str, int]) -> str:
        bag_of_nodes = []
        for node, occurrences in node_occurrences.items():
            for i in range(occurrences):
                bag_of_nodes.append(node)
        return self.embedding_split_char.join(bag_of_nodes)

    def __get_opensearch_client(self) -> OpenSearch:
        host = os.environ.get("OPENSEARCH_HOST")
        port = os.environ.get("OPENSEARCH_PORT")
        auth = (
            os.environ.get("OPENSEARCH_HTTP_AUTH_USER"),
            os.environ.get("OPENSEARCH_HTTP_AUTH_PASSWORD"),
        )

        return OpenSearch(
            hosts=[{"host": host, "port": port}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=False,
        )
