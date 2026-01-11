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
        # Search using iTunes/Deezer API (In par koi block nahi hota)
        search_url = f"https://itunes.apple.com/search?term={query}&limit=1&entity=song"
        response = requests.get(search_url, timeout=10)
        data = response.json()

        if data.get('resultCount', 0) > 0:
            track = data['results'][0]
            return jsonify({
                "status": "success",
                "link": track['previewUrl'],  # Direct MP3 Link
                "title": f"{track['trackName']} - {track['artistName']}"
            })
        
        return jsonify({"status": "error", "message": "Song not found on global servers"}), 404
                
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"}), 500
