# voidarc media sampler

This repository includes utilities for sampling frames and audio snippets from a library of media files (images, video, or audio) and recombining them into a new video. The `sample_media.py` script uses [MoviePy](https://zulko.github.io/moviepy/) to handle processing.

## Requirements

- Python 3.8+
- [`moviepy`](https://pypi.org/project/moviepy/)
- `ffmpeg` installed on your system


Install the Python dependencies with:

```bash
pip install moviepy
pip install ffmpeg
pip install Flask
```

## Usage


### Web App (Recommended)

1. Start the Flask app:
   ```bash
   python app.py
   ```
2. Open your browser and go to the URL shown in your terminal (for GitHub Codespaces, it will look like `https://<your-space>-5000.app.github.dev/`).
3. Use the web interface to sample media and view the latest generated video.

### Command Line

You can also run the script directly:

```
python sample_media/sample_media.py sample_media/library_dir sample_media/output_dir --samples 3 --duration 1.0
```

- `library_dir` is a folder containing supported media files (images, video, or audio) to sample from.
- `output_dir` will contain the extracted frame images, audio snippets, and the generated video files. Each run creates an incremented file like `final_001.mp4`, `final_002.mp4`, and so on.
- `--samples` defines how many random samples to pull from each file.
- `--duration` sets the length (in seconds) of each sampled clip.

## ERC-721 Support

A stub function `fetch_videos_from_erc721` is provided for future integration with Ethereum collections via IPFS. It is currently not implemented. An additional stub `fetch_media_from_erc1155` exists for ERC-1155 collections.

