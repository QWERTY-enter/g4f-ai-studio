from flask import Flask, request, jsonify, Response
import requests
import traceback
import random
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("G4F_API_KEY", "YOUR_G4F_API_KEY_HERE")
BASE_URL = "https://g4f.space/v1"
MAX_MESSAGE_LENGTH = 8000
PROXY_FILE = os.getenv("PROXY_FILE", "/home/workdir/proxy.json")
PROXIES = []

def load_proxies():
    global PROXIES
    try:
        if os.path.exists(PROXY_FILE):
            with open(PROXY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                PROXIES = [p['proxy'] for p in data.get('proxies', []) if p.get('alive') and p.get('proxy')]
                print(f"✅ Loaded {len(PROXIES)} alive proxies")
    except Exception as e:
        print(f"Error: {e}")

load_proxies()

def get_random_proxy():
    return random.choice(PROXIES) if PROXIES else None

def make_request_with_proxy(method, url, **kwargs):
    proxy = get_random_proxy()
    proxies_dict = {"http": proxy, "https": proxy} if proxy else None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if proxies_dict:
                kwargs['proxies'] = proxies_dict
            if method.upper() == 'GET':
                resp = requests.get(url, **kwargs, timeout=30)
            else:
                resp = requests.post(url, **kwargs, timeout=60)
            if resp.status_code in [200, 201]:
                return resp
            elif resp.status_code in [429, 403, 503]:
                time.sleep(2 ** attempt)
                continue
            resp.raise_for_status()
            return resp
        except:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
    raise Exception("Proxy failed")

@app.route('/health')
def health():
    return jsonify({"status": "ok", "proxies_loaded": len(PROXIES)})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    payload = {
        "model": data.get("model", "gpt-4o-mini"),
        "messages": data.get("messages", []),
        "temperature": float(data.get("temperature", 0.7)),
        "max_tokens": int(data.get("max_tokens", 1024)),
        "stream": data.get("stream", True)
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    if payload["stream"]:
        def generate():
            proxy = get_random_proxy()
            proxies_dict = {"http": proxy, "https": proxy} if proxy else None
            with requests.post(f"{BASE_URL}/chat/completions", json=payload, headers=headers, proxies=proxies_dict, stream=True, timeout=90) as resp:
                for chunk in resp.iter_lines():
                    if chunk:
                        yield f"data: {chunk.decode('utf-8', errors='ignore')}\n\n"
        return Response(generate(), mimetype='text/event-stream')
    else:
        resp = make_request_with_proxy('POST', f"{BASE_URL}/chat/completions", json=payload, headers=headers)
        return jsonify(resp.json())

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    payload = {"model": data.get("model", "flux"), "prompt": data.get("prompt"), "n": 1, "response_format": "url"}
    resp = make_request_with_proxy('POST', f"{BASE_URL}/images/generations", json=payload, headers={"Authorization": f"Bearer {API_KEY}"})
    return jsonify(resp.json())

if __name__ == '__main__':
    print("🚀 G4F Backend running")
    app.run(host='0.0.0.0', port=5000)