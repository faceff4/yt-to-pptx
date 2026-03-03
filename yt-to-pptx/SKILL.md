---
name: yt-to-pptx
description: "Turn a YouTube video into a professional presentation. Use this skill whenever a user provides a YouTube link together with a transcript (with timestamps), and wants to generate a PowerPoint (.pptx) slide deck from it. Also trigger when the user says things like 'make slides from this video', 'turn this YouTube into a presentation', 'generate a PPT from this transcript', 'create lecture slides from a video', or any combination of video/transcript + presentation/slides/deck. This skill handles the full pipeline: downloading the video, auto-downloading subtitles from YouTube (or accepting a user-provided transcript), analyzing the transcript to determine slide structure and screenshot timestamps, capturing frames with ffmpeg, and generating a polished .pptx with embedded screenshots using pptxgenjs. Even if the user only provides a YouTube link without a transcript, this skill can attempt to fetch subtitles automatically. If the user only mentions a transcript with timestamps and wants slides, this skill is likely the right choice."
---

# YouTube to Presentation Skill

Turn a YouTube video + timestamped transcript into a polished, multi-slide PowerPoint presentation with auto-captured screenshots.

## When to Use

This skill is designed for the scenario where a user provides:
1. A **YouTube URL** (or an already-downloaded MP4 file)
2. Optionally, a **transcript with timestamps** (e.g., `00:15 大數據不是說一定很大...`)

If no transcript is provided, the skill will attempt to auto-download subtitles from YouTube. If that also fails, the user will be asked to provide one manually.

And wants a `.pptx` slide deck generated from it.

## Prerequisites

Before starting, verify these tools are available. Install any that are missing:

```bash
# Check and install dependencies
which yt-dlp   || pip install yt-dlp --break-system-packages
which ffmpeg   || echo "ffmpeg is required - install via apt/brew"
npm list -g pptxgenjs || npm install -g pptxgenjs react react-dom react-icons sharp
```

## Workflow Overview

The skill follows six phases:

### Phase 1: Obtain the Transcript

There are two ways to get a transcript. Try them in order:

**Option A — User already provided a transcript**: If the user pasted a timestamped transcript, skip ahead to Phase 2.

**Option B — Auto-download from YouTube**: If the user only provided a YouTube link (no transcript), try downloading subtitles automatically:

```bash
# Try traditional Chinese first, then simplified, then auto-generated
yt-dlp --write-auto-sub --sub-lang zh-Hant,zh-Hans,zh --skip-download --sub-format srt -o "subs" "<YOUTUBE_URL>"
```

This will produce an `.srt` file if subtitles exist. Convert the SRT to a simple timestamped transcript format:

```bash
python <skill-path>/scripts/srt_to_transcript.py subs.*.srt > transcript.txt
```

**If no subtitles are available** (yt-dlp outputs nothing), inform the user:

> 「這部影片沒有字幕可以自動下載。請提供逐字稿（含時間軸），我就能繼續幫你做簡報。」

Stop and wait for the user to provide a transcript before proceeding. Do NOT guess or fabricate transcript content.

### Phase 2: Analyze the Transcript

Parse the timestamped transcript to understand the content structure. Identify natural topic breaks that map to individual slides. For each slide, determine:

- **Title** — a concise heading for the topic
- **Key points** — the main ideas covered in that segment
- **Screenshot timestamp** — the best moment to capture a frame (usually when a key visual/diagram/text appears on screen)

When choosing screenshot timestamps, look for moments where the video is likely showing an explanatory graphic, diagram, table, or key text — not a talking head. Prefer timestamps 2-5 seconds *after* a topic starts (giving time for visuals to appear).

Output this analysis as a structured plan before proceeding. Share the plan with the user and get confirmation before moving on.

### Phase 3: Download the Video

```bash
yt-dlp -f "best[height<=720]" -o "video.mp4" "<YOUTUBE_URL>"
```

Use 720p max to keep file size reasonable. The video only needs to be good enough for screenshot extraction.

If the user has already uploaded an MP4 file, skip this step entirely and use the uploaded file.

### Phase 4: Extract Screenshots

Use ffmpeg to capture frames at each planned timestamp:

```bash
# For each timestamp (e.g., 00:15, 01:06, 02:43)
ffmpeg -ss <TIMESTAMP> -i video.mp4 -frames:v 1 -q:v 2 slide_<N>.jpg
```

The `-ss` flag before `-i` enables fast seeking. `-q:v 2` gives high-quality JPEG output.

After extraction, visually inspect the captured frames. If a frame shows a transition or is blurry, adjust the timestamp by ±2 seconds and re-capture.

### Phase 5: Generate the Presentation

Use pptxgenjs (via Node.js) to create the .pptx file.

**Important**: This skill depends on the `pptx` skill for presentation generation. Before writing any pptxgenjs code, ALWAYS read the pptx skill first:

1. Read `/mnt/skills/public/pptx/SKILL.md` — for the overall workflow, design ideas, color palettes, typography, QA process
2. Read `/mnt/skills/public/pptx/pptxgenjs.md` — for the complete pptxgenjs API reference, code patterns, and common pitfalls

Follow all design guidelines from the pptx skill (color palette selection, layout variation, icon usage, spacing, QA steps). This yt-to-pptx skill handles the **video analysis and screenshot pipeline**; the pptx skill handles **how to make the slides look professional**.

#### Slide Structure

A typical presentation from a video follows this pattern:

| Slide | Purpose | Layout |
|-------|---------|--------|
| 1 | Cover / title slide | Dark background, title, subtitle, source attribution |
| 2–N | Content slides | Title bar + screenshot + key points |
| Last | Summary / conclusion | Recap of main points, next steps |

#### Embedding Screenshots

Screenshots should be prominently placed on each content slide. Two recommended layouts:

**Layout A — Screenshot dominant (for visual-heavy content):**
- Screenshot takes ~60% of slide area (right or bottom)
- Key points on the remaining space
- Good for: diagrams, charts, process flows

**Layout B — Text dominant with thumbnail (for concept-heavy content):**
- Key points take main area
- Screenshot as supporting thumbnail (30-40% width, right side)
- Good for: definitions, lists, comparisons

```javascript
// Example: embedding a screenshot
slide.addImage({
  path: "screenshots/slide_03.jpg",
  x: 4.8, y: 1.2, w: 4.8, h: 2.7,  // 16:9 aspect ratio preserved
  shadow: { type: "outer", blur: 6, offset: 3, angle: 135, color: "000000", opacity: 0.15 }
});
```

Always preserve the 16:9 aspect ratio of screenshots. A good default size is `w: 4.8, h: 2.7` inches.

#### Design Guidelines

Follow these principles for a professional result:

- **Color palette**: Choose colors that match the video's topic/domain. Finance → navy/teal/gold. Education → blue/green. Tech → dark/cyan.
- **Consistent layout**: Use a consistent title bar and footer across all content slides.
- **Icons**: Use react-icons to add visual interest to text-heavy slides. Render to PNG via sharp for compatibility.
- **Vary layouts**: Don't use the same layout for every slide. Mix screenshot positions, use cards, grids, and comparison layouts where appropriate.
- **Readable text**: 14-16pt body text, 28-36pt titles. Left-align body text.
- **Don't crowd slides**: Leave breathing room. Not every detail from the transcript needs to be on the slide.

#### Common Pitfalls (pptxgenjs)

- Never use `#` prefix in hex colors — causes file corruption
- Never encode opacity in hex color strings — use `opacity` property
- Never reuse option objects across calls — PptxGenJS mutates them in place
- Use `breakLine: true` between text array items
- Use `bullet: true` for bullet points, never unicode `•`

### Phase 6: QA and Deliver

1. Convert the .pptx to images for visual inspection:
   ```bash
   python scripts/office/soffice.py --headless --convert-to pdf output.pptx
   pdftoppm -jpeg -r 150 output.pdf slide
   ```
2. Inspect key slides visually — check for overlapping elements, cut-off text, low-contrast issues
3. Fix any problems found
4. Copy final file to output directory and present to user

## Tips for Best Results

- **Screenshot selection matters most**: A slide deck with well-chosen screenshots from the video feels like a companion to the video, not just a text summary. Prioritize frames that show diagrams, charts, tables, or key text.
- **Don't transcribe everything**: The slides should capture the essence, not be a verbatim copy of the transcript. Think "study notes" not "court transcript".
- **Attribution**: Always include the video source (channel name, video title, URL) on the cover slide.
- **User confirmation**: After Phase 2 (transcript analysis), share the planned slide structure with the user before proceeding. This saves time if the user wants a different focus or number of slides.

## Example Interaction

**User provides:**
```
YouTube: https://www.youtube.com/watch?v=XXXXX
Transcript:
00:00 今天我們要聊大數據
00:09 大數據必須符合4V特徵
00:15 第一個是大量性，Facebook有2400億張照片
...
```

**Skill produces:**
1. Slide plan with ~10-12 slides
2. Downloaded video → extracted 10-12 screenshots
3. Professional .pptx with embedded screenshots, icons, and structured content
