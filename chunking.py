from pathlib import Path
# from main import records
from pinecone import Pinecone
import os, re
from dotenv import load_dotenv

load_dotenv()
records = []

def chunk_md(text):
    sections = re.split(r'\n(?=## )', text)
    return [i.strip() for i in sections if i.strip()]


for x in Path("knowledge").glob("*.md"):
    text = x.read_text(encoding="utf-8")
    chunks = chunk_md(text)
    
    for i, chunk in enumerate(chunks):
        records.append({
            "_id": f"{x.stem}-{i}",
            "chunk_text": chunk,
            "source": x.name
        })

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("kenzie-knowledge")
index.upsert_records(namespace="kenzie", records=records)