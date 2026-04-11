import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def make_summary(text: str):
    prompt = f"""
Сделай краткое саммари совещания.

Язык: русский.

Требования:
- 5-7 предложений
- только по тексту
- без английского

Текст:
{text}
"""

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "temperature": 0.2,
        "stream": False
    })

    return response.json()["response"]