import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_track_name_from_link(link):
    # Agar Spotify link hai
    if "spotify" in link:
        # Spotify links ko handle karne ke liye simple cleanup
        track_id = link.split('/')[-1].split('?')[0]
        # Hum sirf gaane ka ID le rahe hain, search behtar karne ke liye
        return track_id 
    
    # Agar YouTube link hai
    if "youtube.com" in link or "youtu.be" in link:
        # YouTube se title nikalne ke liye oEmbed use kar rahe hain
        try:
            r = requests.get(f"https://www.youtube.com/oembed?url={link}&format=json")
            return r.json().get('title', '')
        except:
            return ""
    return link

@app.route('/download', methods=['GET'])
def download():
    raw_text = request.args.get('text')
    if not raw_text:
        return jsonify({"status": "error", "message": "No input"}), 400

    # Link se naam nikalna
    search_query = get_track_name_from_link(raw_text)

    try:
        # iTunes/Apple Search
        search_url = f"https://itunes.apple.com/search?term={search_query}&limit=1&entity=song"
        response = requests.get(search_url, timeout=10)
        data = response.json()

        if data.get('resultCount', 0) > 0:
            track = data['results'][0]
            return jsonify({
                "status": "success",
                "link": track['previewUrl'],
                "title": f"{track['trackName']} - {track['artistName']}"
            })
        
        # Agar link se na miley toh user ko batayein
        return jsonify({"status": "error", "message": "Could not extract song from link. Please type the song name directly."}), 404
                
    except Exception as e:
        return jsonify({"status": "error", "message": "Server error"}), 500
