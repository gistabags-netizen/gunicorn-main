import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# Sab domains ko allow karne ke liye CORS set kiya hai
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/download', methods=['GET', 'OPTIONS'])
def download():
    # CORS preflight ke liye
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
        
    query = request.args.get('text')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Search settings ko mazeed behtar kiya gaya hai
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'source_address': '0.0.0.0'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Direct search query use karein
            search_query = f"ytsearch1:{query} audio"
            info = ydl.extract_info(search_query, download=False)
            
            if 'entries' in info and len(info['entries']) > 0:
                video = info['entries'][0]
                return jsonify({
                    "status": "success",
                    "link": video['url'],
                    "title": video['title']
                })
            else:
                return jsonify({"status": "error", "message": "Song not found on servers"}), 404
                
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Vercel ke liye entry point
app.debug = True
