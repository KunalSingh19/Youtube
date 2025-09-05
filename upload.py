import os
import sys
import argparse
import subprocess
import json
import re
import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes required for uploading videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

INSTAGRAM_JSON_FILE = "reelsData.json"
UPLOAD_HISTORY_FILE = "upload_history.json"
TOKEN_FILE = "token.json"
BATCH_SIZE = 65

def get_video_duration(filename: str) -> float:
    """Get video duration in seconds using ffprobe."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries',
             'format=duration', '-of',
             'default=noprint_wrappers=1:nokey=1', filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
        return float(result.stdout)
    except Exception as e:
        print(f"Warning: Could not determine video duration: {e}")
        return -1  # Unknown duration

def get_authenticated_service(client_secrets_file: str):
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=creds)

def initialize_upload(youtube, options):
    body = {
        "snippet": {
            "title": options.title,
            "description": options.description,
            "tags": options.tags if options.tags else None,
            "categoryId": options.category_id
        },
        "status": {
            "privacyStatus": options.privacy_status
        }
    }
    body["snippet"] = {k: v for k, v in body["snippet"].items() if v is not None}
    media = MediaFileUpload(options.file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    print(f"Upload Complete! Video ID: {response['id']}")
    return response['id']

def download_video(url: str, filename: str):
    print(f"Downloading video from {url} ...")
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise Exception(f"Failed to download video, status code: {response.status_code}")
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Video downloaded to {filename}")

def load_instagram_json(json_path: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_upload_history(history_path: str):
    if os.path.exists(history_path):
        with open(history_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}

def save_upload_history(history_path: str, history: dict):
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print(f"Upload history saved to {history_path}")

def extract_tags_from_caption(caption: str):
    tags = re.findall(r'#(\w+)', caption)
    unique_tags = list(dict.fromkeys(tags))
    return unique_tags[:30]

def main():
    parser = argparse.ArgumentParser(description="Download Instagram videos and upload to YouTube")
    parser.add_argument("--client-secrets", required=True, help="Path to client_secrets.json")
    parser.add_argument("--privacy-status", default="private", choices=["public", "private", "unlisted"], help="YouTube video privacy status")
    parser.add_argument("--category-id", default="22", help="YouTube video category ID (default: 22 = People & Blogs)")

    args = parser.parse_args()

    if not os.path.exists(INSTAGRAM_JSON_FILE):
        print(f"Error: Instagram JSON file '{INSTAGRAM_JSON_FILE}' does not exist.")
        sys.exit(1)

    if not os.path.exists(args.client_secrets):
        print(f"Error: Client secrets file '{args.client_secrets}' does not exist.")
        sys.exit(1)

    insta_data = load_instagram_json(INSTAGRAM_JSON_FILE)
    upload_history = load_upload_history(UPLOAD_HISTORY_FILE)
    youtube = get_authenticated_service(args.client_secrets)

    uploaded_count = 0

    for insta_url, post_data in insta_data.items():
        if uploaded_count >= BATCH_SIZE:
            print(f"Reached batch limit of {BATCH_SIZE} videos. Stopping.")
            break

        if insta_url in upload_history:
            print(f"Skipping already uploaded Instagram URL: {insta_url}")
            continue

        try:
            video_url = post_data['media_details'][0]['url']
            description = post_data['post_info'].get('caption', '')
        except (KeyError, IndexError) as e:
            print(f"Error parsing Instagram JSON for {insta_url}: {e}")
            continue

        tags = extract_tags_from_caption(description)
        print(f"Extracted tags from caption: {tags}")

        video_filename = "downloaded_video.mp4"

        try:
            download_video(video_url, video_filename)
        except Exception as e:
            print(f"Error downloading video for {insta_url}: {e}")
            continue

        duration = get_video_duration(video_filename)
        if duration != -1:
            print(f"Video duration: {duration:.2f} seconds")
            if duration <= 60:
                print("Warning: This video is 60 seconds or less and will likely be uploaded as a YouTube Short.")

        class Options:
            pass

        options = Options()
        truncated_title = description[:100]
        options.file = video_filename
        options.title = truncated_title
        options.description = description
        options.privacy_status = args.privacy_status
        options.tags = tags
        options.category_id = args.category_id

        try:
            video_id = initialize_upload(youtube, options)
        except googleapiclient.errors.HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred for {insta_url}:\n{e.content}")
            if os.path.exists(video_filename):
                os.remove(video_filename)
            continue

        upload_history[insta_url] = {
            "youtube_video_id": video_id
        }
        save_upload_history(UPLOAD_HISTORY_FILE, upload_history)

        if os.path.exists(video_filename):
            os.remove(video_filename)
            print(f"Deleted temporary video file {video_filename}")

        uploaded_count += 1

if __name__ == "__main__":
    main()
