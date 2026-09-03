# test_chroma.py

import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    "security_knowledge"
)

print(
    "Document Count:",
    collection.count()
)