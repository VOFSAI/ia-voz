from flask import Flask, render_template

# Linha crucial: cria a instância do Flask
app = Flask(__name__)

# Rota principal
@app.route("/")
def home():
    return "<h1>TESTE OK — Flask está rodando!</h1>"

# Só necessário se rodar localmente (não afeta Render)
if __name__ == "__main__":
    app.run()
