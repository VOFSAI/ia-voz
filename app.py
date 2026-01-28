from flask import Flask, request, send_file
from gtts import gTTS
import uuid
import os

app = Flask(__name__)

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    texto = data.get("texto", "")
    idioma = data.get("idioma", "pt")

    if not texto:
        return "Texto vazio", 400

    filename = f"{uuid.uuid4()}.mp3"
    tts = gTTS(text=texto, lang=idioma)
    tts.save(filename)

    return send_file(filename, mimetype="audio/mpeg")

@app.route("/")
def home():
    return "IA de Voz rodando!"

if __name__ == "__main__":
    app.run()
