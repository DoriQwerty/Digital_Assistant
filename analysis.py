import json
import logging
from ollama_client import ask_ollama, OllamaError

logger = logging.getLogger(__name__)

ANALYSIS_PROMPT = """
Ты — система обработки совещаний.

Проанализируй текст и верни СТРОГО JSON без какого-либо другого текста.

Формат:
{{
  "participants": [
    {{"name": "Имя", "role": "Роль"}}
  ],
  "tasks": [
    {{"task": "что сделать", "assignee": "кто делает"}}
  ]
}}

Правила:
- Только JSON, никакого текста до или после
- Если имя неизвестно — пиши «Спикер 1», «Спикер 2» и т.д.
- Если задач нет — верни "tasks": []
- Минимум 1 участник

Текст:
{text}
"""

SPEAKER_PROMPT = """
Ты редактор расшифровки совещания.

Тебе дали текст после автоматического распознавания речи — в нём могут быть ошибки.

Задача:
1. Исправить очевидные ошибки распознавания.
2. Расставить знаки препинания.
3. Разделить по спикерам, если видна смена говорящего.

Правила:
- Не меняй смысл, не придумывай факты.
- Если не ясно, где сменился спикер — весь текст как «Спикер 1».
- Не добавляй пустых строк и пустых спикеров.
- Только исправленный текст, без объяснений.

Формат:
Спикер 1: текст
Спикер 2: текст

Текст:
{text}
"""

SUMMARY_PROMPT = """
Сделай краткое саммари совещания на русском языке.

Требования:
- 5–7 предложений
- Только по содержанию текста
- Без английских слов

Текст:
{text}
"""


def analyze_text(text: str) -> dict:
    prompt = ANALYSIS_PROMPT.format(text=text)
    try:
        raw = ask_ollama(prompt)
        logger.debug(f"Ответ анализа: {raw[:200]}")
        cleaned = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
    except (OllamaError, json.JSONDecodeError) as e:
        logger.warning(f"Не удалось распарсить анализ: {e}")
        return {"participants": [{"name": "Спикер 1", "role": "Участник"}], "tasks": []}


def make_speaker_transcription(text: str) -> str:
    prompt = SPEAKER_PROMPT.format(text=text)
    try:
        result = ask_ollama(prompt).strip()
        # Убираем пустые строки и «пустые» спикеры вида «Спикер 1:»
        lines = [
            line.strip()
            for line in result.splitlines()
            if line.strip() and not _is_empty_speaker_line(line)
        ]
        return "\n".join(lines) if lines else f"Спикер 1: {text}"
    except OllamaError as e:
        logger.warning(f"Ошибка при форматировании спикеров: {e}")
        return f"Спикер 1: {text}"


def make_summary(text: str) -> str:
    prompt = SUMMARY_PROMPT.format(text=text)
    try:
        return ask_ollama(prompt).strip()
    except OllamaError as e:
        logger.warning(f"Ошибка при создании саммари: {e}")
        return "Не удалось создать саммари."


def _is_empty_speaker_line(line: str) -> bool:
    """Строка вида 'Спикер 1:' без текста после двоеточия."""
    stripped = line.strip()
    return stripped.lower().startswith("спикер") and stripped.endswith(":")
