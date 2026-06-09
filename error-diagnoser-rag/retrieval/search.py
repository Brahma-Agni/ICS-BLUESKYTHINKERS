import pickle
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

FAISS_PATH = BASE_DIR / "faiss_store" / "error_index.faiss"
METADATA_PATH = BASE_DIR / "faiss_store" / "metadata.pkl"

# Load model, index and metadata lazily
model = None
index = None
metadata = None

def load_resources():
    global model, index, metadata
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    if index is None or metadata is None:
        if not FAISS_PATH.exists() or not METADATA_PATH.exists():
            raise FileNotFoundError(f"FAISS index or metadata not found. Please run build_index.py first.")
        index = faiss.read_index(str(FAISS_PATH))
        with open(METADATA_PATH, "rb") as f:
            metadata = pickle.load(f)


def search_error(query, k=1):
    load_resources()
    query_embedding = model.encode([query]).astype("float32")

    distances, indices = index.search(query_embedding, k)

    idx = indices[0][0]

    if idx >= len(metadata):
        return None

    result = metadata[idx]

    return {
        "category": result.get("category", ""),
        "error_type": result.get("error_type", ""),
        "root_cause": result.get("root_cause", ""),
        "solution": result.get("solution", "")
    }


if __name__ == "__main__":

    print("Error Search Ready")
    print("-" * 50)

    while True:

        query = input("\nEnter Error (or 'exit'): ")

        if query.lower() == "exit":
            break

        result = search_error(query)

        print("\nBest Match:\n")
        print(result)