import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery


class Retriever:
    def __init__(self, articles=None):  # 'articles' kept so main.py doesn't break
        self.client = SearchClient(
            endpoint=os.environ["SEARCH_ENDPOINT"],
            index_name=os.environ.get("SEARCH_INDEX", "kb-index"),
            credential=AzureKeyCredential(os.environ["SEARCH_KEY"]),
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
