import random
from pathlib import Path
from typing import List
from moviepy import (
    VideoFileClip,
    ImageClip,
    AudioFileClip,
    ColorClip,
    concatenate_videoclips,
)


def sample_from_media_library(
    library_dir: Path,
    output_dir: Path,
    num_samples_per_file: int = 1,
    sample_duration: float = 1.0,
    color_clip_size: tuple = (640, 480),
) -> Path:
    """Sample clips from media files in a directory and build a new video.

    Parameters
    ----------
    library_dir : Path
        Directory containing source media files.
    output_dir : Path
        Directory where sampled frames, audio, and final video will be written.
    num_samples_per_file : int
        Number of random samples to take from each file.
    sample_duration : float
        Duration of each sample in seconds.

    Returns
    -------
    Path
        Path to the generated mp4 file.
    """
    library_dir = Path(library_dir)
    output_dir = Path(output_dir)
    frames_dir = output_dir / "frames"
    audio_dir = output_dir / "audio"
    frames_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    clips = []
    supported_video = {".mp4", ".mov", ".avi", ".mkv"}
    supported_image = {".jpg", ".jpeg", ".png", ".gif"}
    supported_audio = {".wav", ".mp3", ".aac", ".ogg", ".flac"}

    for media_file in library_dir.iterdir():
        if not media_file.is_file():
            continue
        ext = media_file.suffix.lower()

        for i in range(num_samples_per_file):
            if ext in supported_video:
                clip = VideoFileClip(str(media_file))
                max_start = max(clip.duration - sample_duration, 0)
                start_time = random.uniform(0, max_start)
                if hasattr(clip, "subclip"):
                    sub = clip.subclip(start_time, start_time + sample_duration)
                else:
                    sub = clip.subclipped(start_time, start_time + sample_duration)
            elif ext in supported_image:
                sub = ImageClip(str(media_file)).with_duration(sample_duration)
            elif ext in supported_audio:
                audio_clip = AudioFileClip(str(media_file))
                max_start = max(audio_clip.duration - sample_duration, 0)
                start_time = random.uniform(0, max_start)
                sub_audio = audio_clip.subclip(start_time, start_time + sample_duration)
                sub = ColorClip(size=color_clip_size, color=(0, 0, 0), duration=sample_duration)
                sub = sub.set_audio(sub_audio)
            else:
                continue


            frame_path = frames_dir / f"{media_file.stem}_{i}.png"
            if sub is not None:
                try:
                    sub.save_frame(str(frame_path), t=0)
                except Exception as e:
                    print(f"Error saving frame for {media_file} sample {i}: {e} (type: {type(sub)})")
            else:
                print(f"Warning: sub is None for {media_file} sample {i}")

            if sub.audio:
                audio_path = audio_dir / f"{media_file.stem}_{i}.wav"
                sub.audio.write_audiofile(str(audio_path), logger=None)

            clips.append(sub)

        # Do not close clip or audio_clip here; let moviepy handle it after writing the final video

    if not clips:
        raise ValueError("No media files found in library_dir")

    final_clip = concatenate_videoclips(clips, method="compose")
    final_video_path = output_dir / "final.mp4"
    final_clip.write_videofile(str(final_video_path), codec="libx264", audio_codec="aac")
    final_clip.close()
    for c in clips:
        c.close()
    return final_video_path


def fetch_videos_from_erc721(collection_address: str, destination: Path) -> List[Path]:
    """Placeholder for fetching videos from an ERC-721 collection via IPFS.

    This function is not implemented and exists as a stub for future work.
    """
    raise NotImplementedError("Fetching from ERC-721 collections is not yet implemented.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Sample media frames and audio snippets.")
    parser.add_argument("library", type=Path, help="Directory of media files")
    parser.add_argument("output", type=Path, help="Directory for output files")
    parser.add_argument("--samples", type=int, default=1, help="Samples per file")
    parser.add_argument("--duration", type=float, default=1.0, help="Duration of each sample (seconds)")
    args = parser.parse_args()

    sample_from_media_library(args.library, args.output, args.samples, args.duration)
