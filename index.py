import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['GET'])
def download():
    query = request.args.get('text')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Spotify link ho ya song name, ye dhoond lega
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch',
            'source_address': '0.0.0.0'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Agar Spotify playlist link hai toh ye uski search karega
            info = ydl.extract_info(query, download=False)
            
            if 'entries' in info:
                # Playlist ki surat mein pehla gaana
                video = info['entries'][0]
            else:
                # Single song ki surat mein
                video = info
                
            return jsonify({
                "status": "success",
                "link": video['url'],
                "title": video.get('title', 'Unknown Title')
            })
            
    except Exception as e:
        return jsonify({"status": "error", "message": "Link processing error"}), 500
