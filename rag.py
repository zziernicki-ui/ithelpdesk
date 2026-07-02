# rag.py

from knowledge_base import ARTICLES
from chunker import chunk_articles
from retriever import Retriever
from generator import generate_answer


def main():
    # Chunk articles before retrieval.
    chunks = chunk_articles(ARTICLES, chunk_size=150)
    retriever = Retriever(chunks)
    
    print("RAG troubleshooting assistant (type 'quit' to exit)\n")

    while True:
        query = input("Describe your problem: ").strip()
        if query.lower() in {"quit", "exit"}:
            break
        retrieved = retriever.search(query, top_k=2)
        print("\n" + generate_answer(query, retrieved) + "\n")


if __name__ == "__main__":
    main()