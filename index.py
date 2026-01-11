import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def clean_query(text):
    # Agar ye link hai toh extra kachra saaf karein
    if "spotify.com" in text or "youtube.com" in text or "youtu.be" in text:
        # Link mein se sirf kaam ki cheez nikaalne ki koshish
        text = text.split('/')[-1].split('?')[0]
        text = text.replace('-', ' ').replace('_', ' ')
    return text

@app.route('/download', methods=['GET'])
def download():
    raw_query = request.args.get('text')
    if not raw_query:
        return jsonify({"status": "error", "message": "No input"}), 400

    # Query ko saaf karein taake link bhi search ho sakay
    query = clean_query(raw_query)

    try:
        # Universal Search (iTunes)
        search_url = f"https://itunes.apple.com/search?term={query}&limit=1&entity=song"
        response = requests.get(search_url, timeout=10)
        data = response.json()

        if data.get('resultCount', 0) > 0:
            track = data['results'][0]
            return jsonify({
                "status": "success",
                "link": track['previewUrl'],
                "title": f"{track['trackName']} - {track['artistName']}"
            })
        
        return jsonify({"status": "error", "message": "Link not supported, try searching by name."}), 404
                
    except Exception as e:
        return jsonify({"status": "error", "message": "Server Busy"}), 500
