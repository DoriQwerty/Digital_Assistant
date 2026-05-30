# Digital AI

Веб-приложение для обработки аудиозаписей совещаний

## Стек

- Python, FastAPI
- OpenAI Whisper — распознавание речи
- Ollama (llama3) — анализ текста
- HTML, CSS, JavaScript

## Структура

```
server.py           # запуск сервера
api.py              # эндпоинты
ollama_client.py    # клиент для Ollama
transcription.py    # распознавание речи (Whisper)
analysis.py         # анализ текста, саммари, спикеры
protocol.py         # формирование протокола
requirements.txt    # зависимости
index.html          # интерфейс
styles.css          # стили 
script.js           # js код
```

## Установка

1. Склонировать репозиторий.

2. Создать и активировать виртуальное окружение (ручной способ) либо использовать IDE (автоматический способ):

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Установить и запустить Ollama:

```bash
ollama serve
ollama pull llama3
```

## Запуск

```bash
python server.py
```

Затем открыть `index.html` через локальный сервер:

```bash
python -m http.server 3000
```

И зайти на `http://localhost:3000`.

## Использование

1. Выбрать аудиофайл (mp3, wav, m4a, ogg, flac).
2. Нажать «Обработать».
3. Дождаться результата.
