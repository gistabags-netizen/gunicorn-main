import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# Sab origins ko allow karne ke liye settings
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/download', methods=['GET', 'OPTIONS'])
def download():
    # CORS Preflight request handle karne ke liye
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    query = request.args.get('text')
    if not query:
        return jsonify({"status": "error", "message": "No query"}), 400

    try:
        # iTunes API (Fast & Reliable)
        search_url = f"https://itunes.apple.com/search?term={query}&limit=1&entity=song"
        response = requests.get(search_url, timeout=10)
        data = response.json()

        if data.get('resultCount', 0) > 0:
            track = data['results'][0]
            res = jsonify({
                "status": "success",
                "link": track['previewUrl'],
                "title": f"{track['trackName']} - {track['artistName']}"
            })
            # Headers manually add kar rahe hain security ke liye
            res.headers.add("Access-Control-Allow-Origin", "*")
            return res
        
        return jsonify({"status": "error", "message": "Song not found"}), 404
                
    except Exception as e:
        return jsonify({"status": "error", "message": "Server Busy"}), 500
