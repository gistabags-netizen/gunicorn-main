import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

# Aapki provide ki hui Key
API_KEY = "7a6dd477d7msh7b16b4a874cde7cp1b56e0jsn8d43347e807a"

def get_video_id(text):
    # Agar ye link hai toh ID nikalna
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, text)
    if match:
        return match.group(1)
    
    # Agar link nahi hai toh YouTube se search karke pehla ID uthana
    try:
        search_url = f"https://www.youtube.com/results?search_query={text}"
        html = requests.get(search_url).text
        video_id = re.search(r"\"videoId\":\"([^\"]+)\"", html).group(1)
        return video_id
    except:
        return None

@app.route('/download', methods=['GET'])
def download():
    query = request.args.get('text')
    if not query:
        return jsonify({"status": "error", "message": "No input"}), 400

    video_id = get_video_id(query)
    
    if not video_id:
        return jsonify({"status": "error", "message": "Could not find video"}), 404

    url = "https://youtube-mp36.p.rapidapi.com/dl"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "youtube-mp36.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params={"id": video_id}, timeout=15)
        data = response.json()

        if data.get('status') == 'ok':
            return jsonify({
                "status": "success",
                "link": data.get('link'),
                "title": data.get('title', 'Full Song Download')
            })
        else:
            return jsonify({"status": "error", "message": "API Busy, try again"}), 400
                
    except Exception as e:
        return jsonify({"status": "error", "message": "Server error"}), 500
