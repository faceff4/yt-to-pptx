#!/usr/bin/env python3
"""
Convert an SRT subtitle file to a simple timestamped transcript.

Usage:
  python srt_to_transcript.py input.srt [> output.txt]

Input (SRT format):
  1
  00:00:05,200 --> 00:00:09,100
  大數據不是說一定很大

  2
  00:00:09,100 --> 00:00:15,000
  更重要的是必須符合四種特徵

Output (timestamped transcript):
  00:05 大數據不是說一定很大
  00:09 更重要的是必須符合四種特徵
"""

import re
import sys


def parse_srt(filepath):
    """Parse SRT file and return list of (timestamp_seconds, text) tuples."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into subtitle blocks
    blocks = re.split(r"\n\n+", content.strip())
    entries = []

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        # Parse timestamp line: "00:00:05,200 --> 00:00:09,100"
        time_match = re.match(
            r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->",
            lines[1]
        )
        if not time_match:
            continue

        hours, minutes, seconds, _ = time_match.groups()
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)

        # Join text lines (skip index and timestamp)
        text = " ".join(lines[2:]).strip()
        # Remove HTML tags that sometimes appear in auto-subs
        text = re.sub(r"<[^>]+>", "", text)
        text = text.strip()

        if text:
            entries.append((total_seconds, text))

    return entries


def merge_short_entries(entries, min_gap=2):
    """Merge consecutive entries that are very close together into single lines."""
    if not entries:
        return []

    merged = [entries[0]]
    for ts, text in entries[1:]:
        prev_ts, prev_text = merged[-1]
        # If same timestamp or very close, merge text
        if ts - prev_ts < min_gap and len(prev_text) < 40:
            merged[-1] = (prev_ts, prev_text + " " + text)
        else:
            merged.append((ts, text))

    return merged


def format_timestamp(total_seconds):
    """Format seconds as MM:SS or HH:MM:SS."""
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def srt_to_transcript(filepath):
    """Convert SRT file to timestamped transcript string."""
    entries = parse_srt(filepath)
    entries = merge_short_entries(entries)

    lines = []
    for ts, text in entries:
        lines.append(f"{format_timestamp(ts)} {text}")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        result = srt_to_transcript(filepath)
        print(result)
    except FileNotFoundError:
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)
