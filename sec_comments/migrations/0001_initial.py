# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='comments')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('article', models.ForeignKey(verbose_name='article', to='core.Article')),
                ('parent', models.ForeignKey(default=None, blank=True, to='sec_comments.Comment', null=True, verbose_name='quote')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': 'comment',
                'verbose_name_plural': 'comment',
            },
        ),
    ]
