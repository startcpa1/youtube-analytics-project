from googleapiclient.discovery import build
import os

from datetime import timedelta
import isodate


class GetYoutube:
    """
    Получаем объект для работы с API Youtube
    """
    def __init__(self):
        api_key: str = os.getenv('YT_API_KEY')  # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
        self.youtube = build('youtube', 'v3', developerKey=api_key)  # создать специальный объект для работы с API


class PlayList(GetYoutube):
    """
    Получаем информацию о плейлистах, url, video_id, title
    """
    def __init__(self, playlist_id):
        super().__init__()
        self.playlist_id = playlist_id

        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                                 maxResults=50, ).execute()

        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)).execute()

        self.playlist_info = self.youtube.playlists().list(id=playlist_id, part='snippet,contentDetails',
                                                           maxResults=50).execute()

        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

        self.title = self.playlist_info['items'][0]['snippet']['title']

    @property
    def total_duration(self):
        """
        Вычисляем продолжительность видео в заданном формате
        """
        sum_durations = timedelta(0)

        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            sum_durations += duration

        return sum_durations

    def show_best_video(self):
        """
        Вычисляем самое популярное видео из плейлиста и формируем ссылку
        """
        best_video_id = max(self.video_response['items'], key=lambda item: int(item['statistics']['likeCount']))['id']
        best_video_link = f'https://youtu.be/{best_video_id}'
        return best_video_link
