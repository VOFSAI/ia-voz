from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
import io

app = Flask(__name__)

# Limite de caracteres
MAX_CHARS = 5000

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts():
    try:
        data = request.get_json()
        texto = data.get("texto", "").strip()
        idioma = data.get("idioma", "pt")

        # Limite de caracteres
        if len(texto) == 0:
            return jsonify({"erro": "Texto vazio"}), 400
        if len(texto) > MAX_CHARS:
            texto = texto[:MAX_CHARS]

        # Gera áudio
        tts = gTTS(text=texto, lang=idioma)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        return send_file(mp3_fp, mimetype="audio/mpeg", as_attachment=False, download_name="voz.mp3")

    except Exception as e:
        # Mostra erro real em JSON
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run()
