import whisper

model = whisper.load_model("medium")


def transcribe_audio(file_path: str):
    result = model.transcribe(file_path, language="ru")
    return result["text"]