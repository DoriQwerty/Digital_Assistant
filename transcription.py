import whisper

model = whisper.load_model("small")

def transcribe_audio(file_path: str):
    result = model.transcribe(file_path, language="ru")
    return result["text"]