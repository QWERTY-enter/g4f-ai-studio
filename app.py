from flask import Flask, request, jsonify, Response
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv('G4F_API_KEY', 'YOUR_KEY_HERE')

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Backend running with proxy rotation'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)