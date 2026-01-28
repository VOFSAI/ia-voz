import os
import requests
from flask import Flask, request, send_file, jsonify, render_template
from io import BytesIO

app = Flask(__name__)

# Token do Hugging Face (definido no Render → Environment Variable)
HF_TOKEN = os.getenv("HF_TOKEN")

# Modelo Stable Diffusion (realista)
MODEL_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# Rota principal - frontend
@app.route("/")
def home():
    return render_template("index.html")

# Rota para gerar a imagem
@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.json
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Prompt vazio"}), 400

    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(MODEL_URL, headers=HEADERS, json=payload)

        if response.status_code != 200:
            return jsonify({"error": "Erro ao gerar imagem"}), 500

        image_bytes = BytesIO(response.content)
        image_bytes.seek(0)

        return send_file(
            image_bytes,
            mimetype="image/png",
            as_attachment=False,
            download_name="imagem.png"
        )

    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

# Inicia o app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
