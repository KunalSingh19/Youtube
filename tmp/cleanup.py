import json

# Load the JSON data from a file
with open('upload_history.json', 'r') as f:
    data = json.load(f)

# Iterate over each key and remove the 'youtube_video_id' key if it exists
for key in data:
    if 'youtube_video_id' in data[key]:
        del data[key]['youtube_video_id']

# Save the modified JSON back to a file
with open('upload_history.json', 'w') as f:
    json.dump(data, f, indent=2)
