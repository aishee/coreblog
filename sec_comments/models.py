# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from core.models import Article

# Create your models here.


class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'user')
    article = models.ForeignKey(Article, verbose_name=u'article')
    text = models.TextField(verbose_name=u'comments')
    create_time = models.DateTimeField(u'created', auto_now_add=True)

    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               verbose_name=u'quote')

    class Meta:
        verbose_name_plural = verbose_name = u'comment'
        ordering = ['-create_time']
        app_label = string_with_title('sec_comments', u"Management Comments")

    def __unicode__(self):
        return self.article.title + '_' + str(self.pk)

    __str__ = __unicode__
