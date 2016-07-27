# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('url', models.CharField(max_length=200, null=True, verbose_name='connection', blank=True)),
                ('type', models.CharField(max_length=20, null=True, verbose_name='types', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='updated')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': 'links',
                'verbose_name_plural': 'links',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('text', models.TextField(verbose_name='content')),
                ('url', models.CharField(max_length=200, null=True, verbose_name='connection', blank=True)),
                ('type', models.CharField(max_length=20, null=True, verbose_name='types', blank=True)),
                ('is_read', models.IntegerField(default=0, verbose_name='Read', choices=[(0, 'Unread'), (1, 'Have read')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('from_user', models.ForeignKey(related_name='from_user_notification_set', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='sender')),
                ('to_user', models.ForeignKey(related_name='to_user_notification_set', verbose_name='Recipients', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': 'news',
                'verbose_name_plural': 'news',
            },
        ),
    ]
