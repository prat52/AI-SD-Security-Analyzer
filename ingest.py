import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path


# ---------- CONFIG ----------
PDF_FOLDER = "security_docs"
CHROMA_DB_PATH = "./chroma_db"




BASE_DIR = Path(__file__).resolve().parent

CHROMA_DB_PATH = BASE_DIR / "chroma_db"

print("CHROMA PATH:", CHROMA_DB_PATH)



# ---------- EMBEDDING MODEL ----------
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# ---------- CHROMA ----------
# client = chromadb.PersistentClient(
#     path=CHROMA_DB_PATH
# )
client = chromadb.PersistentClient(
    path=str(CHROMA_DB_PATH)
)

collection = client.get_or_create_collection(
    name="security_knowledge"
)

# ---------- HELPERS ----------

def extract_text(pdf_path):
    text = ""

    reader = PdfReader(pdf_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def chunk_text(text, chunk_size=300):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])

    return chunks


# ---------- INGEST ----------

doc_id = 0

for filename in os.listdir(PDF_FOLDER):

    if not filename.endswith(".pdf"):
        continue

    path = os.path.join(PDF_FOLDER, filename)

    print(f"Processing {filename}")

    text = extract_text(path)

    chunks = chunk_text(text)

    for chunk in chunks:

        embedding = model.encode(
            chunk
        ).tolist()

        collection.add(
            ids=[f"doc_{doc_id}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[
                {
                    "source": filename
                }
            ]
        )

        doc_id += 1

print("Finished ingesting PDFs")