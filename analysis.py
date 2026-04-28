import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_ollama(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "temperature": 0.2,
        "stream": False
    })

    return response.json()["response"]


def analyze_text(text: str):
    prompt = f"""
Ты — система обработки совещаний.

Проанализируй текст и верни СТРОГО JSON.

Формат:
{{
  "participants": [
    {{"name": "Спикер 1", "role": "Участник"}}
  ],
  "tasks": [
    {{"task": "что сделать", "assignee": "кто делает"}}
  ]
}}

Правила:
- Никакого текста кроме JSON
- Если имя неизвестно, пиши Спикер 1, Спикер 2
- Если задач нет, верни "tasks": []
- Минимум 1 участник

Текст:
{text}
"""

    result = ask_ollama(prompt)

    print("RAW LLM:", result)

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:
        return json.loads(result)
    except:
        return {
            "participants": [
                {
                    "name": "Спикер 1",
                    "role": "Участник"
                }
            ],
            "tasks": []
        }


def make_speaker_transcription(text: str):
    prompt = f"""
Ты редактор расшифровки совещания.

Тебе дали текст, который плохо распознала программа.
В нём могут быть ошибки в словах.

Твоя задача:
1. Исправить ошибки распознавания.
2. Сделать текст нормальным и читаемым.
3. Расставить запятые и точки.
4. Разделить текст по спикерам, если видно, что говорит другой человек.

Очень важные правила:
- Исправляй только очевидные ошибки.
- Не меняй смысл.
- Не придумывай новые факты.
- Если непонятно, где сменился человек, оставь всё как Спикер 1.
- Не добавляй пустых спикеров.
- Не пиши "нет текста".
- Не пиши объяснения.
- Не пиши JSON.

Примеры исправлений:
- "Важаемые" → "Уважаемые"
- "прицательным" → "председателем"
- "перспективо" → "перспективы"
- "за спутки" → "за скобки"
- "с респективой" → "с перспективой"

Формат ответа:
Спикер 1: исправленный текст
Спикер 2: исправленный текст

Текст для исправления:
{text}
"""

    try:
        result = ask_ollama(prompt)
        result = result.strip()

        lines = result.split("\n")
        good_lines = []

        for line in lines:
            line = line.strip()

            if line == "":
                continue

            if "нет текста" in line.lower():
                continue

            if line.lower().startswith("спикер") and line.endswith(":"):
                continue

            good_lines.append(line)

        final_text = "\n".join(good_lines)

        if final_text.strip() == "":
            return "Спикер 1: " + text

        return final_text

    except:
        return "Спикер 1: " + text