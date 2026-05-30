import logging
import whisper

logger = logging.getLogger(__name__)

# Загружаем модель один раз при старте сервера
_model = None


def get_model():
    global _model
    if _model is None:
        logger.info("Загружаю Whisper medium...")
        _model = whisper.load_model("medium")
    return _model


def transcribe_audio(file_path: str) -> str:
    model = get_model()
    logger.info(f"Транскрибирую файл: {file_path}")
    result = model.transcribe(file_path, language="ru")
    text = result["text"].strip()
    logger.info(f"Транскрипция готова, длина: {len(text)} символов")
    return text
