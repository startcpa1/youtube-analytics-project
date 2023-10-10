from googleapiclient.discovery import build
import os


class Video:
    def __init__(self, video_id):
        api_key: str = os.getenv('YT_API_KEY')  # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
        youtube = build('youtube', 'v3', developerKey=api_key)  # создать специальный объект для работы с API

        # Получаем информацию о видео
        response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()

        video_info = response['items'][0]
        snippet = video_info['snippet']
        statistic = video_info['statistics']

        self.video_id = video_id
        self.title = snippet['title']
        self.video_link = f'https://www.youtube.com/watch?v={video_id}'
        self.views = int(statistic.get('viewCount', 0))
        self.likes = int(statistic.get('likeCount', 0))

    def __str__(self):  # Возвращаем название видео
        return self.title


class PLVideo(Video):
    """
    Инициализируем метод плейлиста и наследуем класс Video
    """

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
