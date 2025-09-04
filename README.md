
---

# Project README

## Overview

This project contains two scripts:

1. **Instagram Reels Scraper (Node.js)**  
   A script to scrape Instagram Reels URLs from a text file, fetch video data using the `instagram-url-direct` package, and save the results to a JSON file. It supports resuming from the last processed URL, processes URLs in descending order (starting from the last line), and skips URLs that previously failed.

2. **YouTube Video Uploader (Python)**  
   A script to upload videos to YouTube using the YouTube Data API v3. It supports OAuth2 authentication, setting video metadata (title, description, tags, category, privacy), and shows upload progress. It also warns if the video duration is 60 seconds or less (likely a YouTube Short).

---

## 1. Instagram Reels Scraper (Node.js)

### Description

- Reads Instagram Reels URLs from a text file (default: `reels.txt`).
- Processes URLs starting from the last line (descending order).
- Skips URLs that previously failed to fetch.
- Fetches video data using `instagram-url-direct`.
- Saves results to `reelsData.json`.
- Fetches up to 15 successful URLs per run, tries up to 50 URLs to reach that count.
- Removes error entries before saving.

### Requirements

- Node.js (v14+ recommended)
- `instagram-url-direct` package installed (`npm install instagram-url-direct`)

### Usage

```bash
node your_script.js [input_file]
```

- `input_file` (optional): Path to the text file containing Instagram Reels URLs (one per line). Defaults to `reels.txt`.

### Example

```bash
node reelsScraper.js reels.txt
```

### Notes

- The script maintains progress by storing results in `reelsData.json`.
- URLs that previously failed are skipped to avoid repeated errors.
- The script processes URLs in descending order (starting from the last line of the input file).

---

## 2. YouTube Video Uploader (Python)

### Description

- Uploads a video file to YouTube.
- Uses OAuth2 for authentication via a client secrets JSON file.
- Allows setting video title, description, tags, category, and privacy status.
- Shows upload progress.
- Warns if video duration is 60 seconds or less (YouTube Shorts).

### Requirements

- Python 3.6+
- Google API Python Client libraries:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

- `ffprobe` installed and available in your system PATH (part of [FFmpeg](https://ffmpeg.org/)) for video duration detection.

### Usage

```bash
python upload_video.py --file VIDEO_FILE --title "Video Title" --client-secrets client_secrets.json [options]
```

### Arguments

- `--file`: Path to the video file to upload (required).
- `--title`: Video title (required).
- `--description`: Video description (optional).
- `--privacy-status`: Video privacy status (`public`, `private`, `unlisted`). Default: `private`.
- `--tags`: Comma-separated list of tags (optional).
- `--category-id`: YouTube category ID. Default: `22` (People & Blogs).
- `--client-secrets`: Path to OAuth 2.0 client secrets JSON file (required).

### Example

```bash
python upload_video.py --file myvideo.mp4 --title "My Video" --description "Description here" --privacy-status public --tags "tag1,tag2" --client-secrets client_secrets.json
```

### Notes

- The first time you run the script, it will open a browser window to authenticate your Google account.
- Make sure your Google Cloud project has the YouTube Data API enabled.
- The script requires `ffprobe` to detect video duration for warning about Shorts.

---

## Additional Notes

- Both scripts are independent and can be used separately.
- Make sure to install all dependencies and have proper API credentials before running.
- For the Node.js script, consider adding `"type": "module"` in your `package.json` to avoid module warnings.
- For the Python script, ensure your OAuth client secrets file is downloaded from Google Cloud Console.

---

## License

This project is provided as-is without warranty. Use responsibly and respect Instagram and YouTube terms of service.

---
