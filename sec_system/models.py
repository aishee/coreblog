# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

# Create your models here.


IS_READ = {
        0: u'Unread',
        1: u'Have read'
}


class Notification(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'title')
    text = models.TextField(verbose_name=u'content')
    url = models.CharField(max_length=200, verbose_name=u'connection',
                           null=True, blank=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  default=None, blank=True, null=True,
                                  related_name='from_user_notification_set',
                                  verbose_name=u'sender')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='to_user_notification_set',
                                verbose_name=u'Recipients')
    type = models.CharField(max_length=20, verbose_name=u'types',
                            null=True, blank=True)

    is_read = models.IntegerField(default=0, choices=IS_READ.items(),
                                  verbose_name=u'Read')

    create_time = models.DateTimeField(u'created', auto_now_add=True)
    update_time = models.DateTimeField(u'updated', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = u'news'
        ordering = ['-create_time']


class Link(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'title')
    url = models.CharField(max_length=200, verbose_name=u'connection',
                           null=True, blank=True)
    type = models.CharField(max_length=20, verbose_name=u'types',
                            null=True, blank=True)

    create_time = models.DateTimeField(u'created', auto_now_add=True)
    update_time = models.DateTimeField(u'updated', auto_now=True)

    class Meta:
        verbose_name_plural = verbose_name = u'links'
        ordering = ['-create_time']
