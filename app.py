from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)

# =====================================================
# CONFIGURAÇÃO THINGSPEAK
# =====================================================

CHANNEL_ID = "3500867"
API_KEY = "SD5VUIMFJUQ0VSLM"
RESULTS = 200

URL = (
    f"https://api.thingspeak.com/channels/"
    f"{CHANNEL_ID}/feeds.json"
    f"?api_key={API_KEY}"
    f"&results={RESULTS}"
)

# =====================================================
# CAMPOS THINGSPEAK
# =====================================================

FIELD_SOLO = "field1"
FIELD_UMIDADE_AR = "field2"
FIELD_TEMP_AR = "field3"
FIELD_TEMP_AGUA = "field4"
FIELD_QUALIDADE_AGUA = "field5"

# =====================================================
# ROTA PRINCIPAL
# =====================================================

@app.route("/")
def index():
    return render_template("dashboard.html")


# =====================================================
# API DE DADOS
# =====================================================

@app.route("/data")
def data():

    try:

        response = requests.get(URL, timeout=10)
        response.raise_for_status()

        feeds = response.json().get("feeds", [])

        dados = {
            "tempo": [],
            "solo": [],
            "umidade_ar": [],
            "temp_ar": [],
            "temp_agua": [],
            "qualidade_agua": []
        }

        for feed in feeds:

            dados["tempo"].append(
                feed.get("created_at")
            )

            def obter_valor(campo):

                valor = feed.get(campo)

                try:
                    return float(valor)
                except:
                    return None

            dados["solo"].append(
                obter_valor(FIELD_SOLO)
            )

            dados["umidade_ar"].append(
                obter_valor(FIELD_UMIDADE_AR)
            )

            dados["temp_ar"].append(
                obter_valor(FIELD_TEMP_AR)
            )

            dados["temp_agua"].append(
                obter_valor(FIELD_TEMP_AGUA)
            )

            dados["qualidade_agua"].append(
                obter_valor(FIELD_QUALIDADE_AGUA)
            )

        return jsonify(dados)

    except Exception as erro:

        return jsonify({
            "erro": str(erro),
            "tempo": [],
            "solo": [],
            "umidade_ar": [],
            "temp_ar": [],
            "temp_agua": [],
            "qualidade_agua": []
        })


# =====================================================
# HEALTH CHECK
# =====================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "ONLINE",
        "canal": CHANNEL_ID,
        "fonte": "ThingSpeak"
    })


# =====================================================
# EXECUÇÃO
# =====================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
