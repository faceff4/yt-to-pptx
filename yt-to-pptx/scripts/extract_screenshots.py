#!/usr/bin/env python3
"""
Extract screenshots from a video at specified timestamps.

Usage:
  python extract_screenshots.py video.mp4 output_dir "00:09" "00:15" "01:06" "02:43"

Arguments:
  video_path   - Path to the MP4 video file
  output_dir   - Directory to save extracted screenshots
  timestamps   - One or more timestamps in HH:MM:SS or MM:SS format

Each timestamp produces a file named slide_01.jpg, slide_02.jpg, etc.
"""

import subprocess
import sys
import os


def extract_screenshots(video_path, output_dir, timestamps):
    """Extract screenshots from video at given timestamps using ffmpeg."""
    os.makedirs(output_dir, exist_ok=True)

    results = []
    for i, ts in enumerate(timestamps, 1):
        output_path = os.path.join(output_dir, f"slide_{i:02d}.jpg")
        cmd = [
            "ffmpeg", "-y",
            "-ss", ts,
            "-i", video_path,
            "-frames:v", "1",
            "-q:v", "2",
            output_path
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            size = os.path.getsize(output_path)
            results.append({"index": i, "timestamp": ts, "path": output_path, "size": size, "ok": True})
            print(f"  ✓ slide_{i:02d}.jpg  ← {ts}")
        except subprocess.CalledProcessError as e:
            results.append({"index": i, "timestamp": ts, "path": output_path, "ok": False, "error": str(e)})
            print(f"  ✗ slide_{i:02d}.jpg  ← {ts}  FAILED")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    video_path = sys.argv[1]
    output_dir = sys.argv[2]
    timestamps = sys.argv[3:]

    if not os.path.exists(video_path):
        print(f"Error: video file not found: {video_path}")
        sys.exit(1)

    print(f"Extracting {len(timestamps)} screenshots from {video_path}...")
    results = extract_screenshots(video_path, output_dir, timestamps)

    ok_count = sum(1 for r in results if r["ok"])
    print(f"\nDone: {ok_count}/{len(timestamps)} screenshots extracted to {output_dir}/")
