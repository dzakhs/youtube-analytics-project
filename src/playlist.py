import os
from googleapiclient.discovery import build
import datetime
import isodate

class PlayList:
    api_key = os.getenv("API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlists_id):
        self.playlists_id = playlists_id
        self.playlists = self.youtube.playlists().list(id=playlists_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50, ).execute()
        self.title = self.playlists['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlists_id}"

    def get_video(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlists_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    def get_video_statistic(self):
        videos = []
        for video in self.get_video():
            video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                        id=video).execute()

            iso_8601_duration = video_response["items"][0]['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            likes_count = video_response['items'][0]['statistics']['likeCount']
            video_url = f"https://youtu.be/{video}"
            videos.append([duration, likes_count, video_url])

        return videos

    def total_duration(self):
        total = datetime.timedelta()
        for i in self.get_video_statistic():
            total += i[0]
        return total

    def show_best_video(self):
        best_video_url = None
        likes_count = 0
        for i in self.get_video_statistic():
            if int(i[1]) >= likes_count:
                likes_count = int(i[1])
                best_video_url = str(i[2])
        return best_video_url