import json
import os
from googleapiclient.discovery import build


api_key = os.getenv("API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + channel_id
        self.subscribers = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.views = channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        channel = youtube.channels().list(id=self.__channel_id, part='snippet, statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return youtube

    def to_json(self, name):
        data = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers_count": self.subscribers,
            "video_count": self.video_count,
            "view_count": self.views
        }
        with open(name, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    #@property
    #def channel_id(self):
    #    return self.__channel_id
