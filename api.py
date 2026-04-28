from fastapi import APIRouter, UploadFile, File
import shutil
import json
import os
from datetime import datetime

from transcription import transcribe_audio
from analysis import analyze_text, make_speaker_transcription
from summary import make_summary
from protocol import create_protocol

router = APIRouter()


@router.post("/process")
async def process_meeting(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = transcribe_audio(file_path)

        print("TRANSCRIBED TEXT:", text)

        speaker_text = make_speaker_transcription(text)

        print("SPEAKER TEXT:", speaker_text)

        analysis = analyze_text(text)
        summary = make_summary(text)

        data = {
            "transcription": speaker_text,
            "participants": analysis.get("participants", []),
            "tasks": analysis.get("tasks", []),
            "summary": summary
        }

        protocol = create_protocol(data)

        os.makedirs("outputs", exist_ok=True)

        output_name = datetime.now().strftime(
            "outputs/output_%Y-%m-%d_%H-%M-%S.json"
        )

        with open(output_name, "w", encoding="utf-8") as f:
            json.dump(protocol, f, ensure_ascii=False, indent=4)

        return protocol

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)