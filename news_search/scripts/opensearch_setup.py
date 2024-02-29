from opensearchpy import OpenSearch
from utils.opensearch_client import OpenSearchClient

client = OpenSearchClient().client

# Create NewsSearch component index
embedding_analyzer = "embedding_analyzer"
index_body = {
    "settings": {
        "analysis": {
            "analyzer": {
                embedding_analyzer: {
                    "type": "pattern",
                    "pattern": OpenSearchClient.embedding_split_char,
                    "lowercase": True,
                }
            }
        }
    }
}
client.indices.create(OpenSearchClient.index_name, body=index_body)

# Create mappings
mapping_body = {
    "properties": {
        "url": {"type": "text", "analyzer": "keyword"},
        "embedding": {"type": "text", "analyzer": "embedding_analyzer"},
        "text": {"type": "text", "analyzer": "standard"},
    }
}
client.indices.put_mapping(mapping_body, OpenSearchClient.index_name)
