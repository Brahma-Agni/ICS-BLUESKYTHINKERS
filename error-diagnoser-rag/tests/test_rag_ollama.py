import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from retrieval.search import search_error
from api.ollama_client import generate_solution

error_text = "ModuleNotFoundError: No module named pandas"

rag_result = search_error(error_text)

print("RAG RESULT")
print(rag_result)

print("\n" + "=" * 60 + "\n")

response = generate_solution(
    error_text,
    rag_result
)

print(response)