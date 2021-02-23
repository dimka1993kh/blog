from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Post(models.Model):
    title = models.CharField(("Заголовок"), max_length=50, default='')
    text = models.TextField(("Запись"), default='')
    datetime = models.DateTimeField(("Дата и время записи"), default=datetime.datetime.now)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

class Subscribers(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='+')
    subscribe = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='+')
    # def __str__(self):
    #     return self.profile.id
    
    class Meta:
        verbose_name = 'Подписчики'
        verbose_name_plural = 'Подписчики'