import requests
import os

SMALL_MODEL = os.getenv("MODEL")  # по умолчанию "prod"
IP = os.getenv("IP")
response = requests.post(
    f"http://{IP}/api/generate",
    json={
        "model": SMALL_MODEL,
        "prompt": "Объясни что такое Docker простыми словами"
    }
)

print(response.json()["response"])
