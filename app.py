from flask import Flask, render_template, jsonify
import requests
import json
import os

app = Flask(__name__)

# ============================
# CONFIGURAÇÕES THINGSPEAK
# ============================
CHANNEL_ID = "3272763"
API_KEY = "5IIMKO2XDCJ9GT67"
FIELD_UMIDADE = "field1"  # Umidade_Solo
RESULTS = 200

URL = (
    f"https://api.thingspeak.com/channels/"
    f"{CHANNEL_ID}/feeds.json?api_key={API_KEY}&results={RESULTS}"
)

# ============================
# ROTAS
# ============================

@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/data")
def data():
    # Busca dados do ThingSpeak
    response = requests.get(URL)
    feeds = response.json().get("feeds", [])

    x = []
    y = []

    # Processa dados
    for f in feeds:
        if f.get(FIELD_UMIDADE):
            try:
                x.append(f["created_at"])
                y.append(float(f[FIELD_UMIDADE]))
            except ValueError:
                pass

    # Estrutura Plotly
    grafico = {
        "data": [
            {
                "x": x,
                "y": y,
                "type": "scatter",
                "mode": "lines+markers",
                "name": "Umidade do Solo"
            }
        ],
        "layout": {
            "title": "Umidade do Solo (%)",
            "xaxis": {
                "title": "Tempo"
            },
            "yaxis": {
                "title": "Umidade (%)",
                "range": [0, 100]
            }
        }
    }

    # IMPORTANTE: retorna no formato esperado pelo dashboard
    return jsonify([json.dumps(grafico)])


# ============================
# EXECUÇÃO (Render / Local)
# ============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
