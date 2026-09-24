import os
from openai import OpenAI
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pico = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pico.Index("kenzie-knowledge")
ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

question = input("Search: ")


SCORE_THRESHOLD = 0.40

def retrieve(query, top_k=3):
    result = index.search_records(namespace="kenzie", query={
            "inputs": {"text": query}, 
            "top_k": top_k
        },fields=["chunk_text", "source", "section"])
    
    return [i for i in result.result.hits if i.score >= SCORE_THRESHOLD]
# print(result)
# chunks = [i.fields.get("chunk_text", "") for i in result.result.hits ]

# relevant_hits = [i for i in result.result.hits if i.score >= SCORE_THRESHOLD]
relevant_hits = retrieve(question, top_k=3)

if not relevant_hits:
    print("Nao tem resultados relevantes.")
else:
    chunks = [f"[Fuente: {i.fields.get('source')} | Sección: {i.fields.get('section', 'General')}]\n{i.fields.get('chunk_text', '')}" for i in relevant_hits]
    context = "\n\n---\n\n".join(chunks)

    prompt = f"""Basándote únicamente en el contexto proporcionado, responde la siguiente consulta o explica el término consultado. Si la información no guarda ninguna relación con el contexto, responde indicando que no tienes suficiente información.
 
Contexto:
{context}
 
Pregunta: {question}
Al final de tu respuesta agrega:
Fuente: <archivo> — Sección: <sección>
"""
    response = ai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un asistente técnico que responde exclusivamente con el contexto proporcionado."},
            {"role": "user", "content": prompt}
        ]
    )
    print("\n--- Respuesta de GPT ---")
    print(response.choices[0].message.content)

    print("\n--- Fuentes consultadas ---")
for i, match in enumerate(relevant_hits, 1):
    source = match.fields.get("source", "desconocido")
    section = match.fields.get("section", "General")
    print(f"{i}. [Similitud: {match.score:.4f}] Archivo: {source} — Sección: {section}")
