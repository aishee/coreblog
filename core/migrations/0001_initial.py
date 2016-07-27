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
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('en_title', models.CharField(max_length=100, verbose_name='English title')),
                ('img', models.CharField(default=b'/static/img/article/default.jpg', max_length=200)),
                ('tags', models.CharField(help_text='Separated by commas', max_length=200, null=True, verbose_name='label', blank=True)),
                ('summary', models.TextField(verbose_name='Summary')),
                ('content', models.TextField(verbose_name='text')),
                ('view_times', models.IntegerField(default=0)),
                ('zan_times', models.IntegerField(default=0)),
                ('is_top', models.BooleanField(default=False, verbose_name='Sticky')),
                ('rank', models.IntegerField(default=0, verbose_name='Sequence')),
                ('status', models.IntegerField(default=0, verbose_name=b'status', choices=[(0, 'normal'), (1, 'draft'), (2, 'delete')])),
                ('pub_time', models.DateTimeField(default=False, verbose_name='release time')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('author', models.ForeignKey(verbose_name='Author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['rank', '-is_top', '-pub_time', '-create_time'],
                'verbose_name': 'article',
                'verbose_name_plural': 'article',
            },
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('summary', models.TextField(null=True, verbose_name='Summary', blank=True)),
                ('img', models.CharField(default=b'/static/img/carousel/default.jpg', max_length=200, verbose_name='Image Carousel')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('article', models.ForeignKey(verbose_name='article', to='core.Article')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': 'Carousel',
                'verbose_name_plural': 'Carousel',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('rank', models.IntegerField(default=0, verbose_name='Sequence')),
                ('status', models.IntegerField(default=0, verbose_name='status', choices=[(0, 'normal'), (1, 'draft'), (2, 'delete')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('parent', models.ForeignKey(default=None, blank=True, to='core.Category', null=True, verbose_name='Sub-headings')),
            ],
            options={
                'ordering': ['rank', '-create_time'],
                'verbose_name': 'classification',
                'verbose_name_plural': 'classification',
            },
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name='Box contents')),
                ('summary', models.TextField(verbose_name='Summary Box')),
                ('status', models.IntegerField(default=0, verbose_name=b'status', choices=[(0, 'normal'), (1, 'draft'), (2, 'delete')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('article', models.ManyToManyField(to='core.Article', verbose_name='article')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': 'Special column',
                'verbose_name_plural': 'Special column',
            },
        ),
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name='Navigation content')),
                ('url', models.CharField(max_length=200, null=True, verbose_name='At the address', blank=True)),
                ('status', models.IntegerField(default=0, verbose_name='status', choices=[(0, 'normal'), (1, 'draft'), (2, 'delete')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': 'Navigation bar',
                'verbose_name_plural': 'Navigation bar',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('summary', models.TextField(verbose_name='Summary')),
                ('news_from', models.IntegerField(default=0, verbose_name=b'source', choices=[(0, 'oschina'), (1, 'chiphell'), (2, 'freebuf'), (3, 'cnBeta')])),
                ('url', models.CharField(max_length=200, verbose_name='source address')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='source address')),
                ('pub_time', models.DateTimeField(default=False, verbose_name='release time')),
            ],
            options={
                'ordering': ['-title'],
                'verbose_name': 'Information',
                'verbose_name_plural': 'Information',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(verbose_name='classification', to='core.Category'),
        ),
    ]
