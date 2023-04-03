import os
from googleapiclient.discovery import build


class Video:
    api_key = os.getenv("API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, video_id):
        try:
            self.video_id = video_id
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=self.video_id).execute()
            self.title = self.video_response['items'][0]['snippet']['title']
            self.video_url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.view_count = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        except:
            self.title = None
            self.like_count = None
            print("IndexError")


    def __str__(self):
        return self.title



class PLVideo(Video):
    def __init__(self, video_id, playlist_ids):
        super().__init__(video_id)
        self.playlist_ids = playlist_ids