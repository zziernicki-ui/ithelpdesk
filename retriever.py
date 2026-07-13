import os
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery


class Retriever:
    def __init__(self, articles=None):
        self.client = SearchClient(
            endpoint=os.environ["SEARCH_ENDPOINT"],
            index_name=os.environ.get("SEARCH_INDEX", "kb-index"),
            credential=DefaultAzureCredential(),
        )

    def search(self, query, top_k=2):
        results = self.client.search(
            search_text=query,
            vector_queries=[VectorizableTextQuery(
                text=query, k_nearest_neighbors=top_k, fields="text_vector")],
            top=top_k,
        )
        out = []
        for r in results:
            article = {
                "id": r.get("chunk_id", ""),
                "title": r.get("title", "KB article"),
                "content": r.get("chunk", r.get("content", "")),
                "source_id": r.get("title", ""),
                "source_type": "KB",
            }
            out.append((article, r["@search.score"]))
        return out
