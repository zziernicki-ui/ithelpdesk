# generator.py

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

SYSTEM_PROMPT = """You are a technical support assistant. Your job is to synthesize 
troubleshooting advice from knowledge base articles.

Given retrieved KB passages and a user's problem, provide clear, step-by-step 
troubleshooting instructions. Be concise and actionable. Only use information from 
the provided passages—do not add external knowledge."""


def generate_answer(query, retrieved):
    """Use Claude to synthesize an answer from retrieved chunks."""
    
    if not retrieved:
        return "I couldn't find a relevant article for that. Try rephrasing the issue."
    
    # Build context from retrieved chunks.
    context_parts = []
    for article, score in retrieved:
        source_id = article.get("source_id", article["id"])
        source_type = article.get("source_type", "unknown").upper()
        context_parts.append(
            f"[{source_type} - {source_id}]\n{article['content']}"
        )
    
    context = "\n\n".join(context_parts)
    
    # Call Claude.
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"""User problem: {query}

Knowledge base passages:
{context}

Please provide clear troubleshooting steps."""
            }
        ],
    )
    
    answer = message.content[0].text
    
    # Add citations.
    citations = "\n\n--- Sources ---"
    for article, score in retrieved:
        source_id = article.get("source_id", article["id"])
        title = article["title"]
        source_type = article.get("source_type", "unknown").upper()
        citations += f"\n• {title} ({source_type} - {source_id}, relevance: {score:.2f})"
    
    return answer + citations