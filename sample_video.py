import random
from pathlib import Path
from typing import List
from moviepy import VideoFileClip, concatenate_videoclips


def sample_from_library(library_dir: Path, output_dir: Path, num_samples_per_video: int = 1,
                        sample_duration: float = 1.0) -> Path:
    """Sample clips from videos in a directory and build a new video.

    Parameters
    ----------
    library_dir : Path
        Directory containing source video files.
    output_dir : Path
        Directory where sampled frames, audio, and final video will be written.
    num_samples_per_video : int
        Number of random samples to take from each video.
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
    for video_file in library_dir.glob("*.mp4"):
        clip = VideoFileClip(str(video_file))
        for i in range(num_samples_per_video):
            max_start = max(clip.duration - sample_duration, 0)
            start_time = random.uniform(0, max_start)
            sub = clip.subclipped(start_time, start_time + sample_duration)
            frame_path = frames_dir / f"{video_file.stem}_{i}.png"
            sub.save_frame(str(frame_path), t=0)
            audio_path = audio_dir / f"{video_file.stem}_{i}.wav"
            sub.audio.write_audiofile(str(audio_path), logger=None)
            clips.append(sub)

    if not clips:
        raise ValueError("No video files found in library_dir")

    final_clip = concatenate_videoclips(clips)
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
    parser = argparse.ArgumentParser(description="Sample video frames and audio snippets.")
    parser.add_argument("library", type=Path, help="Directory of video files")
    parser.add_argument("output", type=Path, help="Directory for output files")
    parser.add_argument("--samples", type=int, default=1, help="Samples per video")
    parser.add_argument("--duration", type=float, default=1.0, help="Duration of each sample (seconds)")
    args = parser.parse_args()

    sample_from_library(args.library, args.output, args.samples, args.duration)
