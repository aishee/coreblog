# -*- coding: utf-8 -*-
import logging
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from sec_comments.models import Comment
from sec_system.models import Notification
from core.models import Article

ArticleModel = Article
# logger
logger = logging.getLogger(__name__)


# Create your views here.

class CommentControl(View):
    def post(self, request, *args, **kwargs):

        user = self.request.user
     
        text = self.request.POST.get("comment", "")

        if not user.is_authenticated():
            logger.error(
                u'[CommentControl]The current user inactive users:[{}]'.format(
                    user.username
                )
            )
            return HttpResponse(u"Please sign in!", status=403)

        en_title = self.kwargs.get('slug', '')
        try:
            # 默认使用pk来索引(也可根据需要使用title,en_title在索引
            article = ArticleModel.objects.get(en_title=en_title)
        except ArticleModel.DoesNotExist:
            logger.error(u'[CommentControl]This article does not exist:[%s]' % en_title)
            raise PermissionDenied

        # 保存评论
        parent = None
        if text.startswith('@['):
            import ast
            parent_str = text[1:text.find(':')]
            parent_id = ast.literal_eval(parent_str)[1]
            text = text[text.find(':')+2:]
            try:
                parent = Comment.objects.get(pk=parent_id)
                info = u'{}You replied {} comment of'.format(
                    user.username,
                    parent.article.title
                )
                Notification.objects.create(
                    title=info,
                    text=text,
                    from_user=user,
                    to_user=parent.user,
                    url='/article/'+en_title+'.html'
                )
            except Comment.DoesNotExist:
                logger.error(u'[CommentControl]Comments misquoted:%s' % parent_str)
                return HttpResponse(u"Do not modify the code comment!", status=403)

        if not text:
            logger.error(
                u'[CommentControl]The current user enter an empty comment:[{}]'.format(
                    user.username
                )
            )
            return HttpResponse(u"Write your review!", status=403)

        comment = Comment.objects.create(
                user=user,
                article=article,
                text=text,
                parent=parent
                )

        try:
            img = comment.user.img
        except Exception as e:
            img = "http://sdtmta.com/img/user.png"

        print_comment = u"<p>Comment:{}</p>".format(text)
        if parent:
            print_comment = u"<div class=\"comment-quote\">\
                                  <p>\
                                      <a>@{}</a>\
                                      {}\
                                  </p>\
                              </div>".format(
                                  parent.user.username,
                                  parent.text
                              ) + print_comment
        
        html = u"<li>\
                    <div class=\"ai-comment-tx\">\
                        <img src={} width=\"40\"></img>\
                    </div>\
                    <div class=\"ai-comment-content\">\
                        <a><h1>{}</h1></a>\
                        {}\
                        <p>{}</p>\
                    </div>\
                </li>".format(
                    img,
                    comment.user.username,
                    print_comment,
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

        return HttpResponse(html)
