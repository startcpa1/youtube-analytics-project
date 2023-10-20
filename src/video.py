from googleapiclient.discovery import build
import os


class Video:
    api_key: str = os.getenv('YT_API_KEY')  # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    youtube = build('youtube', 'v3', developerKey=api_key)  # создать специальный объект для работы с API

    def __init__(self, video_id):
        # Получаем информацию о видео
        response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                              id=video_id).execute()
        self.response = response

        try:
            self.video_info = self.response['items'][0]
            self.snippet = self.video_info['snippet']
            self.statistic = self.video_info['statistics']

            self.video_id = video_id
            self.title = self.snippet['title']
            self.video_link = f'https://www.youtube.com/watch?v={video_id}'
            self.views = int(self.statistic.get('viewCount', 0))
            self.like_count = int(self.statistic.get('likeCount', 0))
        except Exception:
            self.video_id = video_id
            self.video_info = None
            self.snippet = None
            self.statistic = None
            self.title = None
            self.video_link = None
            self.views = None
            self.like_count = None

    def __str__(self):  # Возвращаем название видео
        return self.title


class PLVideo(Video):
    """
    Инициализируем метод плейлиста и наследуем класс Video
    """

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

