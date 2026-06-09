import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from api.ollama_client import generate_solution

rag_result = {
    "error_type": "ModuleNotFoundError",
    "root_cause": "Package not installed",
    "solution": "Install package using pip"
}

result = generate_solution(
    "ModuleNotFoundError: No module named pandas",
    rag_result
)

print(result)