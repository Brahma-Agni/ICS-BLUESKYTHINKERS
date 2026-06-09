import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
FAISS_DIR = BASE_DIR / "faiss_store"

FAISS_DIR.mkdir(exist_ok=True)

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

all_records = []
embedding_texts = []

# Read all JSON files from data folder
json_files = [
    "python_errors.json",
    "git_errors.json",
    "installation_errors.json",
    "linux_errors.json",
    "database_errors.json"
]

for file_name in json_files:
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        print(f"Skipping missing file: {file_name}")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    for record in records:
        search_text = f"""
        Category: {record.get('category', '')}
        Error: {record.get('error_type', '')}
        Keywords: {' '.join(record.get('keywords', []))}
        Cause: {record.get('root_cause', '')}
        Solution: {record.get('solution', '')}
        """

        embedding_texts.append(search_text)
        all_records.append(record)

print(f"Loaded {len(all_records)} records")

# Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(
    embedding_texts,
    show_progress_bar=True
)

embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS index
faiss_path = FAISS_DIR / "error_index.faiss"
faiss.write_index(index, str(faiss_path))

# Save metadata
metadata_path = FAISS_DIR / "metadata.pkl"

with open(metadata_path, "wb") as f:
    pickle.dump(all_records, f)

print("\nIndex created successfully!")
print(f"Records indexed: {len(all_records)}")
print(f"FAISS file: {faiss_path}")
print(f"Metadata file: {metadata_path}")