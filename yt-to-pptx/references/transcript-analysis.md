# Transcript Analysis Guide

This reference explains how to analyze a timestamped transcript and plan a slide deck from it.

## Input Format

Timestamped transcripts typically look like this:

```
00:00 今天我們要聊大數據
00:09 大數據必須符合4V特徵
00:15 第一個是大量性，Facebook有2400億張照片
```

The timestamp format can vary: `MM:SS`, `HH:MM:SS`, or sometimes just seconds.

## Analysis Steps

### 1. Identify Topic Boundaries

Read through the transcript and mark where the speaker transitions between topics. Look for signals like:

- "接下來我們來聊聊..." (transition phrases)
- "第一個..." "第二個..." (enumeration)
- "舉一個例子..." (example introduction)
- Significant time gaps between lines
- Shift in subject matter

### 2. Group into Slides

Each major topic becomes 1-2 slides. A good rule of thumb:

| Video Length | Typical Slide Count |
|-------------|-------------------|
| 2-5 min     | 6-8 slides        |
| 5-10 min    | 8-14 slides       |
| 10-20 min   | 12-20 slides      |
| 20+ min     | 18-30 slides      |

Always include:
- **Slide 1**: Cover slide (title, source, context)
- **Last slide**: Summary / conclusion / next steps

### 3. Choose Screenshot Timestamps

For each content slide, select the timestamp where the best visual appears. Guidelines:

- **Prefer diagrams/charts**: If the speaker shows a diagram at 01:06, capture that.
- **Offset by +2-3 seconds**: After a topic starts, wait a moment for the visual to fully appear.
- **Avoid transitions**: Don't capture during slide transitions or blank screens.
- **Avoid talking head**: If the video alternates between speaker and visuals, capture the visual moments.

### 4. Output Format

Present the plan as a table:

```
| Slide | Title             | Content Summary           | Screenshot Time | Layout |
|-------|-------------------|---------------------------|-----------------|--------|
| 1     | Cover             | Title, source, context    | -               | dark   |
| 2     | What is Big Data? | Definition, 4V intro      | 00:09           | text+img |
| 3     | The 4V + 1V       | Volume, Variety...        | 00:15           | grid   |
| ...   | ...               | ...                       | ...             | ...    |
```

## Layout Selection Guide

Choose layouts based on the content type of each slide:

- **grid**: Multiple parallel items (e.g., 4V characteristics, 3 types of data)
- **text+img**: One main concept with supporting screenshot
- **comparison**: Before/after, traditional vs new, pros/cons
- **timeline/flow**: Step-by-step processes
- **cards**: 3-4 items with icon + title + description
- **dark**: For cover, section breaks, and conclusion slides
