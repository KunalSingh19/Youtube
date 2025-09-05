
---

# Project README

## Overview

## 1. YouTube Video Uploader (Python)

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
python upload.py --file VIDEO_FILE --title "Video Title" --client-secrets client_secrets.json [options]
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
python upload.py --file myvideo.mp4 --title "My Video" --description "Description here" --privacy-status public --tags "tag1,tag2" --client-secrets client_secrets.json
```

### Notes

- The first time you run the script, it will open a browser window to authenticate your Google account.
- Make sure your Google Cloud project has the YouTube Data API enabled.
- The script requires `ffprobe` to detect video duration for warning about Shorts.

---

## Additional Notes

- Both scripts are independent and can be used separately.
- Make sure to install all dependencies and have proper API credentials before running.
- For the Python script, ensure your OAuth client secrets file is downloaded from Google Cloud Console.

---

## License

This project is provided as-is without warranty. Use responsibly and respect Instagram and YouTube terms of service.

---
