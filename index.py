import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['GET'])
def download():
    query = request.args.get('text')
    if not query:
        return jsonify({"status": "error", "message": "No query provided"}), 400

    try:
        # Search using Deezer API (Very stable for MP3 previews and Spotify searches)
        search_url = f"https://api.deezer.com/search?q={query}&limit=1"
        response = requests.get(search_url, timeout=10)
        data = response.json()

        if data.get('data') and len(data['data']) > 0:
            track = data['data'][0]
            return jsonify({
                "status": "success",
                "link": track['preview'],  # Direct high-quality MP3 preview link
                "title": f"{track['title']} - {track['artist']['name']}"
            })
        
        return jsonify({"status": "error", "message": "Song not found"}), 404
                
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
