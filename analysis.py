import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def analyze_text(text: str):
    prompt = f"""
Ты — система обработки совещаний.

Проанализируй текст и верни СТРОГО JSON.

Язык ответа: русский.

Формат ответа:
{{
  "participants": [
    {{"name": "Имя", "role": "роль"}}
  ],
  "tasks": [
    {{"task": "что сделать", "assignee": "кто делает"}}
  ]
}}

ВАЖНО:
- НИКАКОГО текста вне JSON
- НЕ пиши объяснения
- НЕ пиши на английском
- если нет данных — оставь пустой список []

ДОПОЛНИТЕЛЬНО:
- Если имена не указаны, используй "Спикер 1", "Спикер 2"
- Определи хотя бы одного участника

Текст:
{text}
"""

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "temperature": 0.2,
        "stream": False
    })

    result = response.json()["response"]

    print("RAW LLM:", result)  # 👈 добавь это

    try:
        return json.loads(result)
    except:
        return {"participants": [], "tasks": []}