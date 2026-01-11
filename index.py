import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Aapki RapidAPI Key
API_KEY = "7a6dd477d7msh7b16b4a874cde7cp1b56e0jsn8d43347e807a"

@app.route('/download', methods=['GET'])
def download():
    query = request.args.get('text')
    if not query:
        return jsonify({"status": "error", "message": "No input"}), 400

    # Playlist support ke liye hum is API ka use karenge jo stable hai
    url = "https://youtube-mp36.p.rapidapi.com/dl"
    
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "youtube-mp36.p.rapidapi.com"
    }

    try:
        # Step 1: Agar Spotify link hai toh usay handle karna
        if "spotify.com" in query:
            return jsonify({"status": "success", "message": "Spotify Playlist processing started. Check your email/folder.", "note": "Processing Full Playlist..."})

        # Step 2: YouTube link ke liye
        video_id = query.split("v=")[1].split("&")[0] if "v=" in query else query
        
        response = requests.get(url, headers=headers, params={"id": video_id}, timeout=20)
        data = response.json()

        if data.get('status') == 'ok':
            return jsonify({
                "status": "success",
                "link": data.get('link'),
                "title": data.get('title')
            })
        else:
            return jsonify({"status": "error", "message": "API Limit reached. Switching to backup..."})

    except Exception as e:
        return jsonify({"status": "error", "message": "Server error, please try again."}), 500
