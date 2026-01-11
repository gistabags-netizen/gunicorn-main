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
        return jsonify({"status": "error", "message": "No query"}), 400

    # List of reliable Search APIs
    apis = [
        f"https://itunes.apple.com/search?term={query}&limit=1&entity=song",
        f"https://api.deezer.com/search?q={query}&limit=1"
    ]

    for url in apis:
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            
            # iTunes format check
            if "results" in data and len(data["results"]) > 0:
                track = data["results"][0]
                return jsonify({
                    "status": "success",
                    "link": track["previewUrl"],
                    "title": f"{track['trackName']} - {track['artistName']}"
                })
            
            # Deezer format check
            if "data" in data and len(data["data"]) > 0:
                track = data["data"][0]
                return jsonify({
                    "status": "success",
                    "link": track["preview"],
                    "title": f"{track['title']} - {track['artist']['name']}"
                })
        except:
            continue

    return jsonify({"status": "error", "message": "All servers are busy. Please try a different song name."}), 500
