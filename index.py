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
        return jsonify({"error": "No query provided"}), 400

    try:
        # Alternative Search API (Fast and No-Block)
        search_url = f"https://api.deezer.com/search?q={query}&limit=1"
        response = requests.get(search_url)
        data = response.json()

        if data['data']:
            track = data['data'][0]
            return jsonify({
                "status": "success",
                "link": track['preview'], # Fast preview link
                "title": track['title'] + " - " + track['artist']['name']
            })
        else:
            return jsonify({"status": "error", "message": "Song not found"}), 404
                
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
