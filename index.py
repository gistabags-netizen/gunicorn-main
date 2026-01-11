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
        return jsonify({"status": "error", "message": "No query"}), 400

    try:
        # YouTube search for full song
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1',
            'nocheckcertificate': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Agar link hai ya naam, ye full video dhoondega
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                video = info['entries'][0]
            else:
                video = info
                
            return jsonify({
                "status": "success",
                "link": video['url'], # Full audio link
                "title": video.get('title', 'Full Song')
            })
                
    except Exception as e:
        return jsonify({"status": "error", "message": "YouTube blocked this request. Try again in 1 min."}), 500
