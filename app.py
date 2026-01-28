from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
import io

app = Flask(__name__)
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
        voz = data.get("voz", "female")  # "male" ou "female"

        if len(texto) == 0:
            return jsonify({"erro": "Texto vazio"}), 400
        if len(texto) > MAX_CHARS:
            texto = texto[:MAX_CHARS]

        # Simulação de gênero usando tld
        tld = "com.br" if voz == "female" else "com"
        tts = gTTS(text=texto, lang=idioma, tld=tld)

        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        return send_file(mp3_fp, mimetype="audio/mpeg", as_attachment=False, download_name="voz.mp3")

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run()
