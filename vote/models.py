from django.db import models
from user.models import User

# Create your models here.

class VoteTopic(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'투표 제목', null=False, default=u'제목이 없는 투표')
    contents = models.TextField(max_length=8192, verbose_name=u'투표 내용', null=False, default=u'')
    who_opened = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_closed = models.BooleanField(default=False, verbose_name=u'마감 여부')

    def __unicode__(self):
        result = u'{} (by {})'.format(self.title, self.who_opened)
        if self.is_closed:
            result += u' (마감됨)'
        return result

    def __str__(self):
        return self.__unicode__()

class VoteSelection(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'투표 선택지 이름', null=False, default='제목이 없는 선택지')
    topic = models.ForeignKey(VoteTopic, verbose_name='소속 투표 주제', on_delete=models.CASCADE)
    votedUsers = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return u'{}의 선택지 \'{}\''.format(str(self.topic), self.name)

    def __str__(self):
        return self.__unicode__()
