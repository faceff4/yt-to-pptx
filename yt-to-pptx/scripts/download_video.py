#!/usr/bin/env python3
"""
Download a YouTube video using yt-dlp.

Usage:
  python download_video.py "<YOUTUBE_URL>" [output_path]

Downloads at 720p max to keep file size reasonable for screenshot extraction.
Default output: video.mp4 in current directory.
"""

import subprocess
import sys
import os


def download_video(url, output_path="video.mp4"):
    """Download YouTube video at 720p max."""
    cmd = [
        "yt-dlp",
        "-f", "best[height<=720]",
        "--merge-output-format", "mp4",
        "-o", output_path,
        url
    ]

    print(f"Downloading: {url}")
    print(f"Output: {output_path}")
    print("This may take a moment...\n")

    try:
        subprocess.run(cmd, check=True)
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\n✓ Downloaded successfully: {output_path} ({size_mb:.1f} MB)")
        return True
    except FileNotFoundError:
        print("Error: yt-dlp not found. Install with: pip install yt-dlp")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "video.mp4"
    success = download_video(url, output)
    sys.exit(0 if success else 1)
