from flask import Flask
import os

app = Flask(__name__)

@app.get("/")
def index():
    return {"message": "Hello from Kubernetes!", "status": "ok"}, 200

@app.get("/healthz")
def healthz():
    return "ok", 200

@app.get("/ready")
def ready():
    return "ready", 200

@app.get("/config")
def get_config():
    msg = os.getenv("APP_MESSAGE", "default")
    return {"APP_MESSAGE": msg}, 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
