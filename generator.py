import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-10-21",
)

SYSTEM_PROMPT = """You are a technical support assistant. Your job is to synthesize 
troubleshooting advice from knowledge base articles.

Given retrieved KB passages and a user's problem, provide clear, step-by-step 
troubleshooting instructions. Be concise and actionable. Only use information from 
the provided passages—do not add external knowledge."""


def generate_answer(query, retrieved):
    """Use Azure OpenAI to synthesize an answer from retrieved chunks."""

    if not retrieved:
        return "I couldn't find a relevant article for that. Try rephrasing the issue."

    context_parts = []
    for article, score in retrieved:
        source_id = article.get("source_id", article["id"])
        source_type = article.get("source_type", "unknown").upper()
        context_parts.append(
            f"[{source_type} - {source_id}]\n{article['content']}"
        )

    context = "\n\n".join(context_parts)

    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
        max_tokens=500,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""User problem: {query}

Knowledge base passages:
{context}

Please provide clear troubleshooting steps."""
            },
        ],
    )

    answer = response.choices[0].message.content

    citations = "\n\n--- Sources ---"
    for article, score in retrieved:
        source_id = article.get("source_id", article["id"])
        title = article["title"]
        source_type = article.get("source_type", "unknown").upper()
        citations += f"\n• {title} ({source_type} - {source_id}, relevance: {score:.2f})"

    return answer + citations
