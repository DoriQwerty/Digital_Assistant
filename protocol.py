def create_protocol(data):
    protocol = {
        "date": "auto",
        "participants": data.get("participants", []),
        "summary": data.get("summary", ""),
        "tasks": data.get("tasks", [])
    }
    return protocol