import os 
from dotenv import load_dotenv 
from pinecone import Pinecone

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")

pico = Pinecone(api_key=api_key)

index_name = "kenzie-knowledge"

if not pico.has_index(index_name):
    pico.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model": "llama-text-embed-v2",
            "field_map": {
                "text": "chunk_text"
            }
        }
    )

index = pico.Index(index_name)

# records = [
#     {
#         "_id": "react-1",
#         "chunk_text":"react utiliza componentes para construir interfaces de usuario.",
#         "topic": "react"
#     },
#     {
#         "_id": "nestjs-1",
#         "chunk_text": "Nestjs utiliza dependency injection para administrar las dependencias entre servicios.",
#         "topic": "nestjs"
#     },
#     {
#         "_id": "jwt-1",
#         "chunk_text": "JWT permite representar informacion de autenticacion mediante tokens firmados.",
#         "topic": "authentication"
#     }
# ]

# index.upsert_records(namespace="kenzie", records=records)

print("Datos guardados")