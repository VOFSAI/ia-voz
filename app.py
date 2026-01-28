from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import io

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts():
    try:
        data = request.get_json()
        texto = data.get("texto", "")
        idioma = data.get("idioma", "pt")

        if not texto:
            return jsonify({"erro": "Texto vazio"}), 400

        # Gera áudio
        tts = gTTS(text=texto, lang=idioma)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        return send_file(mp3_fp, mimetype="audio/mpeg", as_attachment=False, download_name="voz.mp3")
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run()
