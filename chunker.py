def chunk_articles(articles, chunk_size=150):
    """
    Split articles into chunks by word count.
    Preserves source file and article ID for citations.
    """
    chunks = []
    
    for article in articles:
        title = article["title"]
        content = article["content"]
        article_id = article.get("id", "unknown")
        
        # Extract source filename from the ID if it exists
        # e.g., "csv_1" -> "csv", "txt_5" -> "txt", "pdf_0" -> "pdf"
        source_type = article_id.split("_")[0] if "_" in article_id else "unknown"
        
        words = content.split()
        
        # Split content into chunks.
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i : i + chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunk = {
                "id": f"{article_id}_chunk_{len(chunks)}",
                "title": title,
                "content": chunk_text,
                "source_id": article_id,
                "source_type": source_type,  # CSV, JSON, TXT, PDF
            }
            chunks.append(chunk)
    
    return chunks