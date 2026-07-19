from flask import Flask, request, jsonify, Response
import os
from dotenv import load_dotenv
from g4f.client import Client

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("G4F_API_KEY")
client = Client(api_key=API_KEY) if API_KEY else Client()

print("🚀 G4F AI Studio Backend (Official Client)")

@app.route('/health')
def health():
    return jsonify({"status": "ok", "mode": "official-g4f-client"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])
    model = data.get("model", "gpt-4o-mini")
    stream = data.get("stream", True)

    if stream:
        def generate():
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                temperature=data.get("temperature", 0.7),
                max_tokens=data.get("max_tokens", 1024)
            )
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield f"data: {chunk.model_dump_json()}\n\n"
        return Response(generate(), mimetype='text/event-stream')
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=data.get("temperature", 0.7),
            max_tokens=data.get("max_tokens", 1024)
        )
        return jsonify(response.model_dump())

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    response = client.images.generate(
        model=data.get("model", "flux"),
        prompt=data.get("prompt"),
        response_format="url"
    )
    return jsonify(response.model_dump())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)