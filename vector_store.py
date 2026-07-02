__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import chromadb


class VectorStore:
    def __init__(self):
        """Initialize in-memory Chroma database."""
        self.client = chromadb.EphemeralClient()
        self.collection = self.client.create_collection(name="articles")
        self.articles = {}  # Store articles by ID for later lookup.

    def add_articles(self, articles):
        """Add articles to Chroma."""
        for article in articles:
            article_id = article["id"]
            text = f"{article['title']} {article['content']}"
            
            # Add to Chroma.
            self.collection.add(ids=[article_id], documents=[text])
            
            # Store the full article for later.
            self.articles[article_id] = article

    def search(self, query, top_k=2):
        """Search and return [(article_dict, score), ...]."""
        results = self.collection.query(query_texts=[query], n_results=top_k)
        
        articles_with_scores = []
        for article_id, distance in zip(results["ids"][0], results["distances"][0]):
            score = 1 - distance  # Convert distance to similarity.
            article = self.articles[article_id]
            articles_with_scores.append((article, score))
        
        return articles_with_scores