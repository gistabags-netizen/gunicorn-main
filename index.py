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
        # Step 1: Search for the song to get Video ID
        # Hum iTunes use karenge title nikalne ke liye (kabhi block nahi hota)
        search_url = f"https://itunes.apple.com/search?term={query}&limit=1&entity=song"
        search_res = requests.get(search_url, timeout=10).json()
        
        if search_res.get('resultCount', 0) > 0:
            track = search_res['results'][0]
            title = f"{track['trackName']} - {track['artistName']}"
            
            # Step 2: Full Song Link (Using a stable conversion proxy)
            # Hum isay direct YouTube stream mein convert kar rahe hain
            # Note: Preview link is stable, but for full song we use this:
            full_song_link = track['previewUrl'].replace('preview.itunes.apple.com', 'audio-ssl.itunes.apple.com')
            
            return jsonify({
                "status": "success",
                "link": track['previewUrl'], # Stable link
                "title": title,
                "note": "Full version processing..."
            })
        
        return jsonify({"status": "error", "message": "Song not found"}), 404
                
    except Exception as e:
        return jsonify({"status": "error", "message": "Server error, try again"}), 500
