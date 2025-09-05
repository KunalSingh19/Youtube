import os
import sys
import argparse
import subprocess
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import google.auth.transport.requests
from google.oauth2.credentials import Credentials

# Scopes required for uploading videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
TOKEN_FILE = "token.json"

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
    # Load existing credentials from token file if it exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(google.auth.transport.requests.Request())
            except Exception as e:
                print(f"Failed to refresh token: {e}")
                creds = None
        if not creds:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=creds)

def initialize_upload(youtube, options):
    body = {
        "snippet": {
            "title": options.title,
            "description": options.description,
            "tags": options.tags.split(",") if options.tags else None,
            "categoryId": options.category_id
        },
        "status": {
            "privacyStatus": options.privacy_status
        }
    }

    # Remove None values from snippet
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

def main():
    parser = argparse.ArgumentParser(description="Upload video to YouTube")
    parser.add_argument("--file", required=True, help="Video file to upload")
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--description", default="", help="Video description")
    parser.add_argument("--privacy-status", default="private", choices=["public", "private", "unlisted"], help="Video privacy status")
    parser.add_argument("--tags", default="", help="Comma separated list of tags")
    parser.add_argument("--category-id", default="22", help="YouTube video category ID (default: 22 = People & Blogs)")
    parser.add_argument("--client-secrets", required=True, help="Path to client_secrets.json")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' does not exist.")
        sys.exit(1)

    if not os.path.exists(args.client_secrets):
        print(f"Error: Client secrets file '{args.client_secrets}' does not exist.")
        sys.exit(1)

    duration = get_video_duration(args.file)
    if duration != -1:
        print(f"Video duration: {duration:.2f} seconds")
        if duration <= 60:
            print("Warning: This video is 60 seconds or less and will likely be uploaded as a YouTube Short.")

    youtube = get_authenticated_service(args.client_secrets)
    try:
        initialize_upload(youtube, args)
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

if __name__ == "__main__":
    main()
