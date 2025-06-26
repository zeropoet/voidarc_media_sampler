import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from flask import Flask, request, jsonify, send_from_directory
from sample_media.sample_media import (
    sample_from_media_library,
    fetch_videos_from_erc721,
    fetch_media_from_erc1155,
)

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
    return "<h1>Welcome to the Void Architecture App!</h1>"

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
    contract = data.get("contract")
    samples = int(data.get("samples", 1))
    duration = float(data.get("duration", 1))

    # Placeholder: in future fetch from ERC-721/1155 using contract address
    # For now we just sample from the local library
    try:
        video_path = sample_from_media_library(LIBRARY_DIR, OUTPUT_DIR, samples, duration)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"video": video_path.name})


# New endpoint for ERC-721 collections
@app.route("/api/erc721", methods=["POST"])
def api_erc721():
    data = request.get_json(force=True)
    contract = data.get("contract")
    if not contract:
        return jsonify({"error": "Missing contract address"}), 400
    try:
        # Fetch videos from ERC-721 contract
        video_paths = fetch_videos_from_erc721(contract, OUTPUT_DIR)
        # Return list of video file names
        return jsonify({"videos": [str(Path(v).name) for v in video_paths]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# New endpoint for ERC-1155 collections
@app.route("/api/erc1155", methods=["POST"])
def api_erc1155():
    data = request.get_json(force=True)
    contract = data.get("contract")
    if not contract:
        return jsonify({"error": "Missing contract address"}), 400
    try:
        # Fetch media from ERC-1155 contract
        media_paths = fetch_media_from_erc1155(contract, OUTPUT_DIR)
        # Return list of media file names
        return jsonify({"media": [str(Path(m).name) for m in media_paths]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
