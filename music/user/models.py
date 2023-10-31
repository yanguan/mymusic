from django.db import models
from django.contrib.auth.models import AbstractUser
from index.models import Song




class Users(models.Model):
    username = models.CharField('用户名', max_length=20, unique=True)
    password = models.CharField(max_length=200)
    mail = models.CharField('邮箱', max_length=30,unique=True)
    votes = models.IntegerField('打榜票数', default=0)
    vote_time = models.CharField('投票时间', max_length=12, default=None, null=True)
    is_vote = models.BooleanField(default=False)
    collect = models.ManyToManyField(Song)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class User_Song(models.Model):
    is_collect = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_song'
