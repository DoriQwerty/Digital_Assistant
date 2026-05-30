from datetime import datetime


def create_protocol(data: dict) -> dict:
    return {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transcription": data.get("transcription", ""),
        "summary": data.get("summary", ""),
        "participants": data.get("participants", []),
        "tasks": data.get("tasks", []),
    }
