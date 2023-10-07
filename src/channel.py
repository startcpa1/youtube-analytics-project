import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # учетные данные приложения
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/aleksandr/dev/keys/seismic-sentry-180215-e4dd0739f7e7.json"

    api_key: str = os.getenv('YT_API_KEY')  # YT_API_KEY скопирован из гугла и вставлен в переменные окружения

    youtube = build('youtube', 'v3', developerKey=api_key)  # создать специальный объект для работы с API

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.channel_id
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        self.printj(self.channel)

    @property
    def channel_id(self):
        """Возвращает id канала"""
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с Youtube API"""
        return cls.youtube

    def to_json(self, filename):
        """Конвертирует в json удобный формат информацию о канале"""
        with open(filename, 'w', encoding='utf-8') as f:
            dict_channel = {
                'channel_id': self.channel_id,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscriber_count': self.subscriber_count,
                'view_count': self.view_count,
                'video_count': self.view_count,
            }
            json.dump(dict_channel, f, ensure_ascii=False)

    def __str__(self):
        return f'{self.title}({self.url})'

    def __add__(self, other):
        """
        Сложение по количеству подписчиков.
        """
        if isinstance(other, Channel):
            total_subscribers = int(self.subscriber_count) + int(other.subscriber_count)
            return f'Всего - {total_subscribers}'
        else:
            raise TypeError('Сложение не поддерживается для данного типа каналов')

    def __sub__(self, other):
        """
        Вычитание по количеству подписчиков.
        """
        if isinstance(other, Channel):
            sub_subcribers = int(self.subscriber_count) - int(other.subscriber_count)
            return f'Разница {sub_subcribers}'
        else:
            raise TypeError('Вычитание не поддерживается для данного типа каналов')

    def __ge__(self, other):
        """
        Сравнение больше или равно
        """
        if isinstance(other, Channel):
            return int(self.subscriber_count) >= int(other.subscriber_count)
        else:
            raise TypeError('Сравнение не поддерживается для данного типа каналов')

    def __le__(self, other):
        """
        Сравнение меньше или равно
        """
        if isinstance(other, Channel):
            return int(self.subscriber_count) <= int(other.subscriber_count)
        else:
            raise TypeError('Сравнение не поддерживается для данного типа каналов')

    def __gt__(self, other):
        """
        Сравнение на больше 1 экземпляра со 2
        """
        if isinstance(other, Channel):
            return int(self.subscriber_count) > int(other.subscriber_count)
        else:
            raise TypeError('Сравнение не поддерживается для данного типа каналов')

    def __lt__(self, other):
        """
        Сравнение на меньше 1 экземпляра со 2
        """
        if isinstance(other, Channel):
            return int(self.subscriber_count) < int(other.subscriber_count)
        else:
            raise TypeError('Сравнение не поддерживается для данного типа каналов')

    def __eq__(self, other):
        """
        Сравнение на равенство 1 экземпляра со 2
        """
        if isinstance(other, Channel):
            if int(self.subscriber_count) == int(other.subscriber_count):
                return True
            else:
                return False
