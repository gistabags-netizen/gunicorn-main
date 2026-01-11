import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Aapki provide ki hui Key
API_KEY = "7a6dd477d7msh7b16b4a874cde7cp1b56e0jsn8d43347e807a"

@app.route('/download', methods=['GET'])
def download():
    query = request.args.get('text')
    if not query:
        return jsonify({"status": "error", "message": "No query"}), 400

    # RapidAPI YouTube DL Endpoint
    url = "https://youtube-mp36.p.rapidapi.com/dl"
    
    # Agar user poora link daalta hai toh ID nikalna
    video_id = query
    if "v=" in query:
        video_id = query.split("v=")[1].split("&")[0]
    elif "youtu.be/" in query:
        video_id = query.split("youtu.be/")[1].split("?")[0]

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "youtube-mp36.p.rapidapi.com"
    }

    try:
        # Requesting Full MP3 Link
        response = requests.get(url, headers=headers, params={"id": video_id}, timeout=15)
        data = response.json()

        if data.get('status') == 'ok':
            return jsonify({
                "status": "success",
                "link": data.get('link'),
                "title": data.get('title', 'Full Song Download')
            })
        else:
            return jsonify({"status": "error", "message": "API Error: Please use a valid YouTube Link"}), 400
                
    except Exception as e:
        return jsonify({"status": "error", "message": "Server error. API Key might be inactive."}), 500
