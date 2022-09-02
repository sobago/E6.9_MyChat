from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    create_datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, verbose_name='Название комнаты')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец комнаты')

    def __str__(self):
        return f'{self.title} [id: {self.pk}]'

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель')
    create_datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=254, verbose_name='Текст сообщения')
    chat = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Идентификатор комнаты')

    def __str__(self):
        return f'{self.text[0:25]} [id: {self.pk}] [Комната: {self.chat}]'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


