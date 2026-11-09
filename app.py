import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import anthropic

app = Flask(__name__)
CORS(app)
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment

HERE = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def home():
    return send_from_directory(HERE, "index.html")

@app.get("/health")
def health():
    return "JARVIS backend is running"

@app.post("/chat")
def chat():
    data = request.get_json(force=True)
    msgs = data.get("messages", [])[-10:]
    memory = "; ".join(data.get("memory", [])) or "none"
    system = ("You are JARVIS, a concise, witty voice assistant. "
              "Reply in 1-3 short sentences. Known facts about the user: " + memory)
    try:
        r = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=300,
            system=system,
            messages=msgs,
        )
        return jsonify(text=r.content[0].text)
    except Exception as e:
        return jsonify(error="Server error: " + str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
