from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "YouTube Stream API is running!"})

@app.route('/get_video_url', methods=['GET'])
def get_video_url():
    video_id = request.args.get('video_id')
    
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            url = info.get('url')

            if url:
                return jsonify({"stream_url": url})
            else:
                return jsonify({"error": "No video URL found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
