import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
IP = os.getenv("IP")
MODEL_NAME = os.getenv("MODEL")

if ENVIRONMENT == "prod":
    OLLAMA_URL = f"http://{IP}:11434/api/generate"
else:
    OLLAMA_URL = "http://localhost:11434/api/generate"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_prompt = data.get("prompt")

    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": user_prompt,
                "stream": False
            }
        )

        result = response.json()

        return jsonify({
            "response": result.get("response"),
            "environment": ENVIRONMENT
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
