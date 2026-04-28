from datetime import datetime


def create_protocol(data):
    protocol = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transcription": data.get("transcription", ""),
        "participants": data.get("participants", []),
        "summary": data.get("summary", ""),
        "tasks": data.get("tasks", [])
    }

    return protocol