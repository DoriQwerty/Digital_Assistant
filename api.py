from fastapi import APIRouter, UploadFile, File
import shutil
import json

from transcription import transcribe_audio
from analysis import analyze_text
from summary import make_summary
from protocol import create_protocol

router = APIRouter()

@router.post("/process")
async def process_meeting(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = transcribe_audio(file_path)
    analysis = analyze_text(text)
    summary = make_summary(text)

    print("TRANSCRIBED TEXT:", text)

    data = {
        "participants": analysis.get("participants", []),
        "tasks": analysis.get("tasks", []),
        "summary": summary
    }

    protocol = create_protocol(data)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(protocol, f, ensure_ascii=False, indent=4)

    return protocol