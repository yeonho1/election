from django.db import models
from user.models import User

# Create your models here.

class VoteTopic(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'투표 제목', null=False, default=u'제목이 없는 투표')
    contents = models.CharField(max_length=8192, verbose_name=u'투표 내용', null=False, default=u'')
    who_opened = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_closed = models.BooleanField(default=False, verbose_name=u'마감 여부')

class VoteSelection(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'투표 선택지 이름', null=False, default='제목이 없는 선택지')
    topic = models.ForeignKey(VoteTopic, verbose_name='소속 투표 주제', on_delete=models.CASCADE)
    votedUsers = models.ManyToManyField(User)
