# 🔍 Error Diagnoser — Vision-Powered RAG Troubleshooting Assistant

> Upload a screenshot of any software error and get AI-powered root cause analysis, step-by-step fix instructions, and best-practice recommendations — all running **100% locally** via Ollama.

---

## 📌 Overview

**Error Diagnoser** is a locally-run, full-stack AI application that combines:

- 🖼️ **Vision LLM** (`qwen2.5vl`) — extracts error type and message directly from screenshots
- 🗄️ **FAISS RAG** (`all-MiniLM-L6-v2` embeddings) — retrieves the most semantically similar known error from a curated knowledge base
- 🧠 **Language LLM** (`llama3.2`) — synthesizes the extracted error + RAG context into structured, actionable troubleshooting steps
- 🌐 **Flask Web Server** — serves a browser-based dashboard UI and exposes a REST API

No cloud APIs. No data leaves your machine.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📸 Screenshot Upload | Drag & drop or select any error screenshot (JPEG, PNG, WEBP) |
| 🔎 Vision Extraction | `qwen2.5vl` identifies `error_type` and `error_message` from the image |
| 📚 RAG Retrieval | FAISS vector search matches against a pre-built error knowledge base |
| 🤖 AI Fix Generation | `llama3.2` generates cause, fix steps, verification, severity & alternatives |
| 📊 Confidence Score | Each diagnosis includes a confidence score and severity rating |
| 💡 Best Practices | Recommendations to prevent the same error in future |
| 🖥️ Browser Dashboard | Beautiful frontend UI served directly by Flask |

---

## 🏗️ Project Structure

```
or-file/
├── app.py                        # Flask server — main entry point
├── index.html                    # Frontend dashboard UI
├── dashboard_bg.png              # UI background asset
├── requirements.txt              # Root-level Python dependencies
├── .env                          # Environment variables (not committed)
├── .gitignore
│
├── services/
│   └── extractor.py              # Vision extraction via qwen2.5vl + Ollama
│
└── error-diagnoser-rag/          # RAG sub-module
    ├── config.py
    ├── requirements.txt          # RAG-specific dependencies
    ├── api/
    │   └── ollama_client.py      # LLM solution generation via llama3.2
    ├── retrieval/
    │   └── search.py             # FAISS semantic search
    ├── embeddings/               # Embedding generation scripts
    ├── faiss_store/
    │   ├── error_index.faiss     # Pre-built FAISS index
    │   └── metadata.pkl          # Error metadata store
    ├── data/                     # Source error knowledge base (CSV/JSON)
    └── tests/                    # Unit & integration tests
```

---

## ⚙️ How It Works

```
User uploads screenshot
        │
        ▼
[1] services/extractor.py
    → qwen2.5vl (Ollama Vision)
    → Returns: { error_type, error_message }
        │
        ▼
[2] error-diagnoser-rag/retrieval/search.py
    → Encodes query with all-MiniLM-L6-v2
    → FAISS nearest-neighbor search
    → Returns: { category, root_cause, solution }
        │
        ▼
[3] error-diagnoser-rag/api/ollama_client.py
    → llama3.2 (Ollama LLM)
    → Returns: { cause, fix_steps, verify, severity, confidence_score, alternatives, recommendation }
        │
        ▼
[4] Flask API → JSON response → index.html Dashboard
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10+**
- [Ollama](https://ollama.com/) installed and running locally
- The following Ollama models pulled:

```bash
ollama pull qwen2.5vl
ollama pull llama3.2
```

---

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd or-file
```

---

### 2. Install Root Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Install RAG Sub-module Dependencies

```bash
pip install -r error-diagnoser-rag/requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root (or update the existing one):

```env
# Add any custom configuration here
# e.g., custom Ollama host if not running on localhost
OLLAMA_HOST=http://localhost:11434
```

---

### 5. Verify the FAISS Store Exists

The `error-diagnoser-rag/faiss_store/` directory must contain:
- `error_index.faiss`
- `metadata.pkl`

If these are missing, rebuild the index from your error knowledge base data in `error-diagnoser-rag/data/`.

---

### 6. Run the Application

```bash
python app.py
```

The server starts on **`http://localhost:5000`**. Open this in your browser to access the dashboard.

---

## 🔌 API Reference

### `POST /api/extract-error`

Accepts a screenshot image and returns a full AI-powered diagnosis.

**Request:**
```
Content-Type: multipart/form-data
Field: image  (file — JPEG, PNG, or WEBP)
```

**Response:**
```json
{
  "error_type": "ModuleNotFoundError",
  "error_message": "No module named 'flask'",
  "root_cause": "The required Python package is not installed in the active environment.",
  "solution": "Install the missing package using pip.",
  "ai_fix": {
    "cause": "The virtual environment does not have Flask installed.",
    "fix_steps": [
      "Activate your virtual environment: source venv/bin/activate",
      "Install Flask: pip install flask"
    ],
    "verify": "Run python -c 'import flask' to confirm successful import."
  },
  "confidence_score": 0.95,
  "confidence": 95,
  "severity": "Medium",
  "alternatives": ["Use conda: conda install flask"],
  "recommendation": "Always use a virtual environment and maintain a requirements.txt."
}
```

### `GET /`

Serves the frontend dashboard UI (`index.html`).

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Web Framework** | Flask 3.0.3 |
| **CORS** | flask-cors 4.0.1 |
| **Vision LLM** | qwen2.5vl via Ollama |
| **Text LLM** | llama3.2 via Ollama |
| **Vector Search** | FAISS (faiss-cpu) |
| **Embeddings** | sentence-transformers (`all-MiniLM-L6-v2`) |
| **Environment** | python-dotenv |
| **HTTP Client** | requests |

---

## 🧪 Running Tests

```bash
cd error-diagnoser-rag
python -m pytest tests/
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| `Connection refused` on port `11434` | Ensure Ollama is running: `ollama serve` |
| `Model not found` error | Pull the required models: `ollama pull qwen2.5vl && ollama pull llama3.2` |
| FAISS index not found | Rebuild the index from the data in `error-diagnoser-rag/data/` |
| `JSON decode error` from vision model | The model returned non-JSON output; try increasing the image quality or clarity |
| Slow response times | Vision + LLM inference is CPU-bound; response times of 15–60s are normal without a GPU |

---

## 📄 License

This project is open source. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Ollama](https://ollama.com/) — local LLM runtime
- [Qwen2.5-VL](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct) — vision-language model
- [Meta Llama 3.2](https://llama.meta.com/) — text generation model
- [FAISS](https://github.com/facebookresearch/faiss) — efficient similarity search
- [Sentence Transformers](https://www.sbert.net/) — semantic embeddings

