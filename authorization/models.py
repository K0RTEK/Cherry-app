import os

from django.contrib.auth.models import User
from django.db import models
import os


def get_user_upload_path(instance, filename):
    # instance - объект модели, который содержит информацию о файле (например, AudioFile)
    # filename - имя загружаемого файла

    # Получите уникальный идентификатор пользователя, например, его username или ID
    user_identifier = str(instance.user.username)  # Пример: username пользователя

    # Создайте полный путь к файлу, включая имя файла, без добавления "Серега/"
    return os.path.join('audio', user_identifier, filename)


def audio_upload_path(instance, filename):
    filename = os.path.basename(filename)
    return filename


class AudioFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=get_user_upload_path,
        default='path_to_default_file.mp3'
    )
    audio = models.FileField(upload_to=get_user_upload_path)
    result = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.audio)
