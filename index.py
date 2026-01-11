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

    try:
        # Step 1: Search for the video ID using an open API
        search_url = f"https://vid.puffyan.us/api/v1/search?q={query}"
        search_res = requests.get(search_url, timeout=15).json()
        
        if not search_res:
            return jsonify({"status": "error", "message": "Song not found"}), 404
            
        video_id = search_res[0]['videoId']
        title = search_res[0]['title']

        # Step 2: Get the direct audio link (Full Song)
        # Hum Invidious ki public API use kar rahe hain jo block nahi hoti
        stream_url = f"https://vid.puffyan.us/api/v1/videos/{video_id}"
        video_data = requests.get(stream_url, timeout=15).json()
        
        # Sab se behtareen audio format nikalna
        audio_url = video_data['adaptiveFormats'][0]['url']

        return jsonify({
            "status": "success",
            "link": audio_url,
            "title": title
        })
                
    except Exception as e:
        return jsonify({"status": "error", "message": "High Traffic. Please try again in a moment."}), 500
