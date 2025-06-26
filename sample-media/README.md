# SAMPLE-MEDIA

This repository includes utilities for sampling frames and audio snippets from a library of media files (images, video, or audio) and recombining them into a new video. The `sample_media.py` script uses [MoviePy](https://zulko.github.io/moviepy/) to handle processing.

## Requirements

- Python 3.8+
- [`moviepy`](https://pypi.org/project/moviepy/)
- `ffmpeg` installed on your system

Install the Python dependencies with:

```bash
pip install moviepy
pip install ffmpeg-python
```

## Usage

```
python sample-media/sample_media.py sample-media/library_dir sample-media/output_dir --samples 3 --duration 1.0
```

- `library_dir` is a folder containing supported media files (images, video, or audio) to sample from.
- `output_dir` will contain the extracted frame images, audio snippets, and the final video `final.mp4`.
- `--samples` defines how many random samples to pull from each file.
- `--duration` sets the length (in seconds) of each sampled clip.

## ERC-721 Support

A stub function `fetch_videos_from_erc721` is provided for future integration with Ethereum collections via IPFS. It is currently not implemented.
