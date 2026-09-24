import re, os
from dotenv import load_dotenv
from pinecone import Pinecone
from pathlib import Path

load_dotenv()

def extract_chunks_with_sections(md_text, filename):
    sections = re.split(r'\n(?=## )', md_text)
    records = []
    for key,value in enumerate(sections):
        lines = value.strip().split('\n')
        heading = lines[0].replace('#', '').strip() if lines[0].startswith('#') else "General"
        records.append({
            "_id": f"{filename}-{key}",
            "chunk_text": value.strip(),
            "source": filename,
            "section": heading
        })
    return records

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("kenzie-knowledge")

all_records = []

for file_path in Path("knowledge").glob("*.md"):
    content = file_path.read_text(encoding="utf-8")
    chunks = extract_chunks_with_sections(content, file_path.name)
    all_records.extend(chunks)

index.upsert_records(namespace="kenzie", records=all_records)
print(f"✅ Ingestión completada: {len(all_records)} chunks guardados con sus secciones.")