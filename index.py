import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# Sab domains ko ijazat dainay ke liye
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/download', methods=['GET', 'OPTIONS'])
def download():
    # CORS Preflight request ko handle karna zaroori hai
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    query = request.args.get('text')
    if not query:
        return jsonify({"status": "error", "message": "No query"}), 400

    try:
        # iTunes API (Sab se ziada stable)
        search_url = f"https://itunes.apple.com/search?term={query}&limit=1&entity=song"
        response = requests.get(search_url, timeout=10)
        data = response.json()

        if data.get('resultCount', 0) > 0:
            track = data['results'][0]
            # Headers manually add kar rahe hain takay WordPress block na ho
            response_data = jsonify({
                "status": "success",
                "link": track['previewUrl'],
                "title": f"{track['trackName']} - {track['artistName']}"
            })
            response_data.headers.add("Access-Control-Allow-Origin", "*")
            return response_data
        
        return jsonify({"status": "error", "message": "Song not found"}), 404
                
    except Exception as e:
        return jsonify({"status": "error", "message": "Server Busy"}), 500
