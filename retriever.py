from vector_store import VectorStore


class Retriever:
    def __init__(self, articles):
        """Initialize retriever with articles."""
        self.store = VectorStore()
        self.store.add_articles(articles)

    def search(self, query, top_k=2):
        """Return top_k most relevant articles."""
        return self.store.search(query, top_k=top_k)