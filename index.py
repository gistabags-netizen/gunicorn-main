import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/download', methods=['GET'])
def download():
    query = request.args.get('text')
    if not query:
        return jsonify({"status": "error", "message": "No input"}), 400

    try:
        # iTunes API kabhi block nahi hoti aur ye Spotify ke 100% gaane dhoond leti hai
        search_url = f"https://itunes.apple.com/search?term={query}&limit=1&entity=song"
        response = requests.get(search_url, timeout=10)
        data = response.json()

        if data.get('resultCount', 0) > 0:
            track = data['results'][0]
            return jsonify({
                "status": "success",
                "link": track['previewUrl'], # Fast MP3 Link
                "title": f"{track['trackName']} - {track['artistName']}"
            })
        
        # Agar iTunes par na miley toh Deezer backup
        backup_url = f"https://api.deezer.com/search?q={query}&limit=1"
        backup_res = requests.get(backup_url).json()
        if backup_res.get('data'):
            track = backup_res['data'][0]
            return jsonify({
                "status": "success",
                "link": track['preview'],
                "title": f"{track['title']} - {track['artist']['name']}"
            })

        return jsonify({"status": "error", "message": "Song not found on any server"}), 404
                
    except Exception as e:
        return jsonify({"status": "error", "message": "Server Busy, try again"}), 500
