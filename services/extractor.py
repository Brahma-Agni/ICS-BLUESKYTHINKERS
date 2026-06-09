import base64
import json
import logging
import requests
OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5vl"  # Points to the model ran by user
def extract_error_from_image(image_file) -> dict:
    """
    Processes an uploaded image file, calls Qwen2.5-VL:3b via Ollama,
    and returns structured error fields.
    """
    try:
        img_bytes = image_file.read()
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
        prompt = (
            "Analyze the uploaded screenshot. Your task is to identify software-related errors.\n"
            "Extract:\n"
            "- error_type\n"
            "- error_message\n\n"
            "Rules:\n"
            "- Focus only on error information.\n"
            "- Ignore UI elements, buttons, menus, timestamps, and unrelated text.\n"
            "- If a stack trace exists, use it to determine the error type.\n"
            "- Return ONLY a valid JSON object matching this format, with absolutely nothing else:\n"
            "{\n"
            '  "error_type": "Error Name",\n'
            '  "error_message": "Complete Error Message"\n'
            "}"
        )
        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [img_b64]
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.0
            }
        }
        logging.info(f"Invoking Ollama Vision service with model target: {MODEL}...")
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        if response.status_code != 200:
            raise Exception(f"Ollama backend service returned an error: {response.text}")
        response_data = response.json()
        llm_output = response_data.get("message", {}).get("content", "").strip()
        logging.info(f"Raw Vision LLM Output: {llm_output}")
        if llm_output.startswith("```"):
            lines = llm_output.splitlines()
            if lines and lines[0].startswith("```"):
                lines.pop(0)
            if lines and lines[-1].startswith("```"):
                lines.pop()
            llm_output = "\n".join(lines).strip()
        structured_json = json.loads(llm_output)
        return {
            "error_type": structured_json.get("error_type", "UnknownError"),
            "error_message": structured_json.get("error_message", "Could not extract full error message context.")
        }
    except json.JSONDecodeError:
        raise ValueError(f"Model response did not yield valid structured data. Raw output: {llm_output}")
    except Exception as e:
        raise e