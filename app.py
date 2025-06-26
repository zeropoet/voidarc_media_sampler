
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from sample_media.sample_media import sample_from_media_library

app = Flask(__name__)
BASE_DIR = Path(__file__).parent
LIBRARY_DIR = BASE_DIR / "sample_media" / "library_dir"
OUTPUT_DIR = BASE_DIR / "sample_media" / "output_dir"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def latest_video() -> Path | None:
    videos = sorted(OUTPUT_DIR.glob("final_*.mp4"))
    return videos[-1] if videos else None

@app.route("/")
def home():
    return '''
    <html>
    <head>
        <title>Void Architecture App</title>
        <style>
            body { font-family: Arial, sans-serif; background: #000; color: #eee; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 40px auto; background: #000; border-radius: 10px; box-shadow: 0 2px 8px #000; padding: 2em; }
            h1 { color: #eee; }
            .form-row { display: flex; gap: 1em; align-items: flex-end; margin-bottom: 1em; }
            .form-row label { display: flex; flex-direction: column; font-weight: normal; margin: 0; }
            input, button { margin-top: 0.5em; padding: 0.5em; border-radius: 5px; border: none; }
            button { background: #eee; color: #000; font-weight: bold; cursor: pointer; }
            button:hover { background: #ffd580; }
            .video-section { margin-top: 2em; }
            video { width: 100%; border-radius: 8px; background: #000; }
            .error { color: #ff6666; margin-top: 1em; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Void Architecture Media-Sample App</h1>
            <form id="sampleForm">
                <div class="form-row">
                    <label>Samples:
                        <input type="number" id="samples" name="samples" value="3" min="1" max="10" required />
                    </label>
                    <label>Duration (seconds):
                        <input type="number" id="duration" name="duration" value="1.0" min="0.1" step="0.1" required />
                    </label>
                    <button type="submit">Sample Media</button>
                </div>
            </form>
            <div class="error" id="errorMsg"></div>
            <div class="video-section" id="videoSection" style="display:none;">
                <h2>Latest Video</h2>
                <video id="latestVideo" controls></video>
            </div>
        </div>
        <script>
        async function fetchLatestVideo() {
            const res = await fetch('/videos');
            const data = await res.json();
            if (data.video) {
                document.getElementById('videoSection').style.display = '';
                document.getElementById('latestVideo').src = '/videos/' + data.video;
            } else {
                document.getElementById('videoSection').style.display = 'none';
            }
        }
        document.getElementById('sampleForm').onsubmit = async function(e) {
            e.preventDefault();
            document.getElementById('errorMsg').textContent = '';
            const samples = document.getElementById('samples').value;
            const duration = document.getElementById('duration').value;
            try {
                const res = await fetch('/api/sample', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ samples: Number(samples), duration: Number(duration) })
                });
                const data = await res.json();
                if (res.ok && data.video) {
                    await fetchLatestVideo();
                } else {
                    document.getElementById('errorMsg').textContent = data.error || 'Unknown error.';
                }
            } catch (err) {
                document.getElementById('errorMsg').textContent = err.message;
            }
        };
        window.onload = fetchLatestVideo;
        </script>
    </body>
    </html>
    '''

@app.route("/videos")
def get_latest_video():
    vid = latest_video()
    return jsonify({"video": vid.name if vid else None})


@app.route("/videos/<path:filename>")
def serve_video(filename):
    return send_from_directory(OUTPUT_DIR, filename)


@app.route("/api/sample", methods=["POST"])
def api_sample():
    data = request.get_json(force=True)

    samples = int(data.get("samples", 1))
    duration = float(data.get("duration", 1))
    try:
        video_path = sample_from_media_library(LIBRARY_DIR, OUTPUT_DIR, samples, duration)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"video": video_path.name})





if __name__ == "__main__":
    app.run(debug=True)
