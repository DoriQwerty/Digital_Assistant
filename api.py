import json
import logging
import os
import tempfile
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File

from analysis import analyze_text, make_speaker_transcription, make_summary
from protocol import create_protocol
from transcription import transcribe_audio

logger = logging.getLogger(__name__)

router = APIRouter()

ALLOWED_EXTENSIONS = {"mp3", "wav", "m4a", "ogg", "flac"}
OUTPUTS_DIR = "outputs"


def _get_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


@router.post("/process")
async def process_meeting(file: UploadFile = File(...)):
    ext = _get_extension(file.filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый формат файла. Допустимые: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Сохраняем во временный файл — он удалится автоматически
    with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
        tmp_path = tmp.name
        content = await file.read()
        tmp.write(content)

    try:
        logger.info(f"Начинаю обработку файла: {file.filename}")

        text = transcribe_audio(tmp_path)
        speaker_text = make_speaker_transcription(text)
        analysis = analyze_text(text)
        summary = make_summary(text)

        protocol = create_protocol({
            "transcription": speaker_text,
            "participants": analysis.get("participants", []),
            "tasks": analysis.get("tasks", []),
            "summary": summary,
        })

        _save_protocol(protocol, file.filename)

        return protocol

    except Exception as e:
        logger.exception(f"Ошибка при обработке файла {file.filename}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def _save_protocol(protocol: dict, original_filename: str) -> None:
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_name = os.path.splitext(original_filename)[0]
    output_path = os.path.join(OUTPUTS_DIR, f"{base_name}_{timestamp}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(protocol, f, ensure_ascii=False, indent=4)
    logger.info(f"Протокол сохранён: {output_path}")
