# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class string_with_title(str):
    """ Admin to modify the app name displayed, because admin app name is str.title() display,
    Therefore, methods to modify the title str class can be achieved.
    """
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self

# Create your models here.
STATUS = {
        0: u'normal',
        1: u'draft',
        2: u'delete',
}

#News from
NEWS = {
        0: u'X1',
        1: u'X2',
        2: u'X3',
        3: u'X4',
}


class Nav(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'Navigation content')
    url = models.CharField(max_length=200, blank=True, null=True,
                           verbose_name=u'At the address')

    status = models.IntegerField(default=0, choices=STATUS.items(),
                                 verbose_name=u'status')
    create_time = models.DateTimeField(u'Created', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u"Navigation bar"
        ordering = ['-create_time']
        app_label = string_with_title('core', u"Management blog")

    def __unicode__(self):
        return self.name

    __str__ = __unicode__


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'name')
    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               verbose_name=u'Sub-headings')
    rank = models.IntegerField(default=0, verbose_name=u'Sequence')
    status = models.IntegerField(default=0, choices=STATUS.items(),
                                 verbose_name=u'status')

    create_time = models.DateTimeField(u'Created', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'classification'
        ordering = ['rank', '-create_time']
        app_label = string_with_title('core', u"Management blog")

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('category-detail-view', args=(self.name,))

    def __unicode__(self):
        if self.parent:
            return '%s-->%s' % (self.parent, self.name)
        else:
            return '%s' % (self.name)

    __str__ = __unicode__


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'Author')
    category = models.ForeignKey(Category, verbose_name=u'classification')
    title = models.CharField(max_length=100, verbose_name=u'title')
    en_title = models.CharField(max_length=100, verbose_name=u'English title')
    img = models.CharField(max_length=200,
                           default='/static/img/article/default.jpg')
    tags = models.CharField(max_length=200, null=True, blank=True,
                            verbose_name=u'label', help_text=u'Separated by commas')
    summary = models.TextField(verbose_name=u'Summary')
    content = models.TextField(verbose_name=u'text')
    view_times = models.IntegerField(default=0)
    zan_times = models.IntegerField(default=0)

    is_top = models.BooleanField(default=False, verbose_name=u'Sticky')
    rank = models.IntegerField(default=0, verbose_name=u'Sequence')
    status = models.IntegerField(default=0, choices=STATUS.items(),
                                 verbose_name='status')
    pub_time = models.DateTimeField(default=False, verbose_name=u'release time')
    create_time = models.DateTimeField(u'Created', auto_now_add=True)
    update_time = models.DateTimeField(u'Updated', auto_now=True)

    def get_tags(self):
        tags_list = self.tags.split(',')
        while '' in tags_list:
            tags_list.remove('')

        return tags_list

    class Meta:
        verbose_name_plural = verbose_name = u'article'
        ordering = ['rank', '-is_top', '-pub_time', '-create_time']
        app_label = string_with_title('core', u"Management blog")

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('article-detail-view', args=(self.en_title,))

    def __unicode__(self):
            return self.title

    __str__ = __unicode__


class Column(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'Box contents')
    summary = models.TextField(verbose_name=u'Summary Box')
    article = models.ManyToManyField(Article, verbose_name=u'article')
    status = models.IntegerField(default=0, choices=STATUS.items(),
                                 verbose_name='status')
    create_time = models.DateTimeField(u'Created',
                                       auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'Special column'
        ordering = ['-create_time']
        app_label = string_with_title('core', u"Management blog")

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('column-detail-view', args=(self.name,))

    def __unicode__(self):
        return self.name

    __str__ = __unicode__


class Carousel(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'title')
    summary = models.TextField(blank=True, null=True, verbose_name=u'Summary')
    img = models.CharField(max_length=200, verbose_name=u'Image Carousel',
                           default='/static/img/carousel/default.jpg')
    article = models.ForeignKey(Article, verbose_name=u'article')
    create_time = models.DateTimeField(u'Created', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'Carousel'
        ordering = ['-create_time']
        app_label = string_with_title('core', u"Management blog")


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'title')
    summary = models.TextField(verbose_name=u'Summary')
    news_from = models.IntegerField(default=0, choices=NEWS.items(),
                                    verbose_name='source')
    url = models.CharField(max_length=200, verbose_name=u'source address')
    create_time = models.DateTimeField(u'source address', auto_now_add=True)
    pub_time = models.DateTimeField(default=False, verbose_name=u'release time')

    class Meta:
        verbose_name_plural = verbose_name = u'Information'
        ordering = ['-title']
        app_label = string_with_title('core', u"Management blog")

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('news-detail-view', args=(self.pk,))

    def __unicode__(self):
        return self.title

    __str__ = __unicode__
