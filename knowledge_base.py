# knowledge_base.py

import json
import csv
import os
from pathlib import Path


def load_articles():
    """Load all articles from kb_data folder (CSV, JSON, TXT, PDF)."""
    articles = []
    
    for filename in os.listdir("kb_data"):
        path = f"kb_data/{filename}"
        
        if filename.endswith(".csv"):
            with open(path) as f:
                for row in csv.DictReader(f):
                    articles.append(row)
        
        elif filename.endswith(".json"):
            with open(path) as f:
                articles.extend(json.load(f))
        
        elif filename.endswith(".txt"):
            with open(path) as f:
                sections = f.read().split("---")
                for idx, section in enumerate(sections):
                    lines = section.strip().split("\n", 1)
                    if len(lines) == 2:
                        articles.append({
                            "id": f"txt_{idx}",
                            "title": lines[0].strip(),
                            "content": lines[1].strip(),
                        })
        
        elif filename.endswith(".pdf"):
            try:
                import pdfplumber
                with pdfplumber.open(path) as pdf:
                    for idx, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text:
                            lines = text.split("\n", 1)
                            articles.append({
                                "id": f"pdf_{idx}",
                                "title": lines[0] if lines else f"Page {idx}",
                                "content": lines[1] if len(lines) > 1 else text,
                            })
            except ImportError:
                print("pdfplumber not installed, skipping PDFs")
    
    return articles


ARTICLES = load_articles()