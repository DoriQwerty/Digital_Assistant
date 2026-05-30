import logging
import requests

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"


class OllamaError(Exception):
    pass


def ask_ollama(prompt: str, temperature: float = 0.2) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.Timeout:
        raise OllamaError("Ollama не ответил за 120 секунд")
    except requests.exceptions.ConnectionError:
        raise OllamaError("Не удалось подключиться к Ollama. Убедись, что сервис запущен")
    except (KeyError, ValueError) as e:
        raise OllamaError(f"Неожиданный ответ от Ollama: {e}")
