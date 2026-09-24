import os, json
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI
 
load_dotenv()
 
pico = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pico.Index("kenzie-knowledge")
ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 
SCORE_THRESHOLD = 0.40

with open("eval_dataset.json", "r", encoding="utf-8") as f:
    TEST_DATASET=json.load(f)
# TEST_DATASET = [
#     {
#         "query": "¿Qué es Git y para qué sirve?",
#         "expected_source": "introducao_git_github.md",
#         "should_answer": True
#     },
#     {
#         "query": "¿Cuáles son las diferencias entre Git y GitHub?",
#         "expected_source": "introducao_git_github.md",
#         "should_answer": True
#     },
#     {
#         "query": "¿Para qué sirve la etiqueta <p> en HTML?",
#         "expected_source": "introduccion_html.md",
#         "should_answer": True
#     },
#     {
#         "query": "¿Cómo preparar una pizza?",
#         "expected_source": None,
#         "should_answer": False
#     },
#     {
#         "query": "¿Cómo configurar un servidor con Docker?",
#         "expected_source": None,
#         "should_answer": False
#     }
# ]

def run_rag(question):
    result = index.search_records(
        namespace="kenzie",
        query={"inputs": {"text": question}, "top_k": 3}
    )
    relevant_hits = [i for i in result.result.hits if i.score >= SCORE_THRESHOLD]

    if not relevant_hits:
        return {"answered": False, "sources": [], "response": "nao tem resultados relevantes."}

    sources = [i.fields.get("source") for i in relevant_hits]
    chunks = [i.fields.get("chunk_text", "") for i in relevant_hits]
    context = "\n\n---\n\n".join(chunks)

    prompt = f"""Basándote únicamente en el contexto proporcionado, responde la siguiente consulta o explica el término consultado. Si la información no guarda ninguna relación con el contexto, responde exactamente: "NO_INFO".
 
Contexto:
{context}
 
Pregunta: {question}
"""
    
    res = ai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]

    )
    content = res.choices[0].message.content.strip()
    answered = "NO_INFO" not in content and "nao tem suficiente informacao" not in content.lower()
    return {"answered": answered, "sources": sources, "response": content}

print("=== INICIANDO EVALUACIÓN DEL RAG ===\n")
total = len(TEST_DATASET)
passed = 0

for idx, test in enumerate(TEST_DATASET, 1):
    q = test["query"]
    print(f"[{idx}/{total}] Pregunta: {q}")
    out = run_rag(q)
 
    # Verificar recuperación y respuesta
    retrieval_ok = True
    if test["expected_source"]:
        retrieval_ok = test["expected_source"] in out["sources"]
    
    decision_ok = (out["answered"] == test["should_answer"])
 
    if retrieval_ok and decision_ok:
        passed += 1
        print("  Resultado: PASÓ ✅")
    else:
        print("  Resultado: FALLÓ ❌")
        print(f"  - Fuentes obtenidas: {out['sources']}")
        print(f"  - Respuesta: {out['response'][:80]}...")
 
    print("-" * 50)
 
print(f"\nResumen: {passed}/{total} pruebas superadas ({(passed/total)*100:.1f}%)")