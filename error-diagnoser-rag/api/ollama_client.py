import json
import logging
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def generate_solution(error_text, rag_result):
    prompt = f"""
You are an expert software troubleshooting assistant.

User Error:
{error_text}

Retrieved Knowledge:
Error Type: {rag_result.get('error_type', 'Unknown')}
Root Cause: {rag_result.get('root_cause', 'Unknown')}
Solution: {rag_result.get('solution', 'No solution found')}

Analyze the error and the retrieved knowledge. Produce a troubleshooting diagnosis in the following exact JSON schema:
{{
  "cause": "A concise explanation of why the error occurs.",
  "fix_steps": [
    "Step 1 to resolve the error",
    "Step 2 to resolve the error"
  ],
  "verify": "A verification step or command to confirm the error is fixed.",
  "confidence_score": 0.95,
  "severity": "Low|Medium|High|Critical",
  "alternatives": [
    "Alternative fix or command if the primary solution doesn't apply",
    "Another optional workaround"
  ],
  "recommendation": "Best practice recommendation to avoid this issue in the future."
}}

You MUST return ONLY a valid JSON object matching the schema above. Do not include any introductory or concluding text, and do not wrap it in markdown code blocks.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "format": "json",
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        
        result_text = response.json().get("response", "").strip()
        return json.loads(result_text)
    except Exception as e:
        logging.error(f"Error calling Ollama or parsing response: {str(e)}")
        # Construct a robust fallback dictionary using the RAG result
        cause = rag_result.get("root_cause", "Root cause could not be analyzed automatically.")
        solution = rag_result.get("solution", "Review the error details and try standard resolution steps.")
        
        fix_steps = [s.strip() for s in solution.split(";") if s.strip()]
        if not fix_steps:
            fix_steps = [solution]
            
        return {
            "cause": cause,
            "fix_steps": fix_steps,
            "verify": "Confirm that the application or command now executes without the error.",
            "confidence_score": 0.85,
            "severity": "Medium",
            "alternatives": ["Check online documentation for: " + (rag_result.get("error_type") or "this error")],
            "recommendation": "Ensure your dependencies and configuration files are properly set up."
        }