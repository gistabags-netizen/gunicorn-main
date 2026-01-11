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

    # Invidious Instances jo Full Song allow karti hain
    instances = [
        "https://inv.tux.sh",
        "https://invidious.sethforprivacy.com",
        "https://vid.puffyan.us"
    ]

    for base in instances:
        try:
            # Step 1: Search Video ID
            search_url = f"{base}/api/v1/search?q={query}"
            search_res = requests.get(search_url, timeout=5).json()
            if not search_res: continue
            
            video_id = search_res[0]['videoId']
            title = search_res[0]['title']

            # Step 2: Get Audio Link (Full Song)
            video_url = f"{base}/api/v1/videos/{video_id}"
            video_data = requests.get(video_url, timeout=5).json()
            
            # Sub se behtareen audio link nikalna
            audio_link = video_data['adaptiveFormats'][0]['url']
            
            return jsonify({
                "status": "success",
                "link": audio_link,
                "title": title
            })
        except:
            continue

    return jsonify({"status": "error", "message": "Servers busy. Try again after 1 minute."}), 500
