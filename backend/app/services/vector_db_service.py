import os
from pathlib import Path


from sentence_transformers import SentenceTransformer
import chromadb



BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DB_PATH = BASE_DIR / "chroma_db"

print("CHROMA PATH:", CHROMA_DB_PATH)



# Load once at startup
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# client = chromadb.PersistentClient(
#     path="./chroma_db"
# )
client = chromadb.PersistentClient(
    path=str(CHROMA_DB_PATH)
)

collection = client.get_or_create_collection(
    "security_knowledge"
)
print(
    "Collection Count:",
    collection.count()
)


def get_security_context(
    architecture_text: str,
    top_k: int = 5
) -> str:

    query_embedding = model.encode(
        architecture_text
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    print("RAW CHROMA RESULTS:")
    print(results)

    docs = results["documents"][0]
    print("\n========== USER QUERY ==========")
    print(architecture_text)

    print("\n========== RETRIEVED DOCS ==========")

    for i, doc in enumerate(docs, start=1):
        print(f"\n--- DOC {i} ---")
        print(doc[:500])

    context = "\n\n".join(docs)

    return context