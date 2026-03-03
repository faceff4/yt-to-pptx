# yt-to-pptx

> Claude Skill — 把 YouTube 影片自動變成專業簡報

提供 YouTube 連結（+逐字稿），自動下載影片、擷取截圖、生成 PowerPoint 簡報。

## 環境需求（必裝）

使用前請先確認已安裝以下工具，**缺一不可**：

```bash
# 1. 安裝 yt-dlp（下載 YouTube 影片與字幕）
pip install yt-dlp

# 2. 安裝 ffmpeg（影片截圖）
#    Windows: https://ffmpeg.org/download.html 下載後加入 PATH
#    Mac:
brew install ffmpeg
#    Linux:
sudo apt install ffmpeg

# 3. 安裝 Node.js 套件（生成簡報）
npm install -g pptxgenjs react react-dom react-icons sharp
```

> ⚠️ **Windows 用戶注意**：ffmpeg 需要手動下載並加入系統 PATH，否則截圖功能無法運作。  
> 教學：下載 ffmpeg → 解壓縮 → 把 `bin` 資料夾路徑加到系統環境變數的 PATH 中。

確認安裝成功：
```bash
yt-dlp --version
ffmpeg -version
node -v
```

三個指令都有回應版本號就可以開始使用了。

---

## 功能特色

- **自動抓字幕**：優先從 YouTube 下載繁中/簡中字幕，不需要手動提供逐字稿
- **智慧分頁**：根據逐字稿內容自動規劃簡報架構
- **自動截圖**：用 ffmpeg 在最佳時間點擷取影片畫面
- **專業簡報**：搭配 pptx skill，生成有設計感的 .pptx 檔案
- **中文友善**：針對繁體中文影片優化

## 使用流程

```
使用者提供 YouTube 連結
        ↓
自動下載字幕（或使用者提供逐字稿）
        ↓
分析內容 → 規劃分頁 → 截圖時間點
        ↓
下載影片 → ffmpeg 批次截圖
        ↓
pptxgenjs 生成簡報 + 嵌入截圖
        ↓
輸出 .pptx 檔案
```

## 安裝方式

### 方法一：直接安裝 .skill 檔

從 [Releases](../../releases) 下載 `yt-to-pptx.skill`，然後在 Claude 設定中匯入。

### 方法二：手動安裝

將 `yt-to-pptx/` 資料夾複製到你的 Claude skills 目錄中。

## 搭配使用

這個 skill 搭配 **pptx skill** 一起使用效果最好。yt-to-pptx 負責影片處理流程，pptx skill 負責簡報設計規範。

## 使用範例

在 Claude 中直接說：

> 「幫我把這個 YouTube 影片做成簡報」
> https://www.youtube.com/watch?v=XXXXXXXXX

或提供逐字稿：

> 「根據這個逐字稿做成 10 頁簡報」
> 00:00 今天我們要聊大數據
> 00:09 大數據必須符合4V特徵
> ...

## 檔案結構

```
yt-to-pptx/
├── SKILL.md                        # 主要指令文件
├── scripts/
│   ├── download_video.py           # YouTube 影片下載
│   ├── extract_screenshots.py      # ffmpeg 批次截圖
│   └── srt_to_transcript.py        # SRT 字幕轉時間軸逐字稿
└── references/
    └── transcript-analysis.md      # 逐字稿分析指南
```

## 授權

MIT License