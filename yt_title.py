
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_video_info(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    try:
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        items = response.get('items', [])
        if items:
            video_info = items[0]
            print(video_info)
            title = video_info['snippet']['title']
            # thumbnail_url = video_info['snippet']['thumbnails']['default']['url']
            return title

    except HttpError as e:
        print(f'Error retrieving video info for video ID {video_id}: {e}')

    return None, None

# Specify the video ID and API key
# video_id = "lKYBB-Uw1IM"
api_key = "AIzaSyBMpLFsUCmJI1dSW1YM2ZHEZ5JHYGsjRCM"

# Retrieve video information
# title = get_video_info(video_id, api_key)

# Print the title of the video
# if title:
#     print("Title:", title)
    
