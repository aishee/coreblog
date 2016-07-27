# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import (base36_to_int, is_safe_url,
                               urlsafe_base64_decode, urlsafe_base64_encode)
from sec_auth.forms import SecUserCreationForm, SecPasswordRestForm
from sec_auth.models import SecUser
from sec_system.models import Notification
import time
import datetime
from PIL import Image
import os
import json
import base64
import logging

logger = logging.getLogger(__name__)

# Create your views here.


class UserControl(View):

    def post(self, request, *args, **kwargs):
        
        slug = self.kwargs.get('slug')

        if slug == 'login':
            return self.login(request)
        elif slug == "logout":
            return self.logout(request)
        elif slug == "register":
            return self.register(request)
        elif slug == "changepassword":
            return self.changepassword(request)
        elif slug == "forgetpassword":
            return self.forgetpassword(request)
        elif slug == "changetx":
            return self.changetx(request)
        elif slug == "resetpassword":
            return self.resetpassword(request)
        elif slug == "notification":
            return self.notification(request)

        raise PermissionDenied

    def get(self, request, *args, **kwargs):
    
        raise Http404

    def login(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)

        errors = []

        if user is not None:
            auth.login(request, user)
        else:
            errors.append(u"Password or user name is incorrect")

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def logout(self, request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]The user does not log in')
            raise PermissionDenied
        else:
            auth.logout(request)
            return HttpResponse('OK')

    def register(self, request):
        username = self.request.POST.get("username", "")
        password1 = self.request.POST.get("password1", "")
        password2 = self.request.POST.get("password2", "")
        email = self.request.POST.get("email", "")

        form = SecUserCreationForm(request.POST)

        errors = []
     
        if form.is_valid():
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            title = u"Welcome to {} ！".format(site_name)
            message = "".join([
                u"Hello there! {} ,Thanks for registration {} ！\n\n".format(username, site_name),
                u"Keep in mind the following information:\n",
                u"Username: {}\n".format(username),
                u"Mailbox: {}\n".format(email),
                u"Website：http://{}\n\n".format(domain),
            ])
            from_email = None
            try:
                send_mail(title, message, from_email, [email])
            except Exception as e:
                logger.error(
                    u'[UserControl]Register failed to send message:[{}]/[{}]'.format(
                        username, email
                    )
                )
                return HttpResponse(u"Send mail error!\nRegistration failed", status=500)

            new_user = form.save()
            user = auth.authenticate(username=username, password=password2)
            auth.login(request, user)

        else:
            
            for k, v in form.errors.items():
             
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def changepassword(self, request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]The user does not log in')
            raise PermissionDenied

        form = PasswordChangeForm(request.user, request.POST)

        errors = []

        if form.is_valid():
            user = form.save()
            auth.logout(request)
        else:
    
            for k, v in form.errors.items():
              
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def forgetpassword(self, request):
        username = self.request.POST.get("username", "")
        email = self.request.POST.get("email", "")

        form = SecPasswordRestForm(request.POST)

        errors = []


        if form.is_valid():
            token_generator = default_token_generator
            from_email = None
            opts = {
                    'token_generator': token_generator,
                    'from_email': from_email,
                    'request': request,
                   }
            user = form.save(**opts)

        else:
      
            for k, v in form.errors.items():
  
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

    def resetpassword(self, request):
        uidb64 = self.request.POST.get("uidb64", "")
        token = self.request.POST.get("token", "")
        password1 = self.request.POST.get("password1", "")
        password2 = self.request.POST.get("password2", "")

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = SecUser._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, SecUser.DoesNotExist):
            user = None

        token_generator = default_token_generator

        if user is not None and token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            errors = []
            if form.is_valid():
                user = form.save()
            else:
            
                for k, v in form.errors.items():
               
                    errors.append(v.as_text())

            mydict = {"errors": errors}
            return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )
        else:
            logger.error(
                u'[UserControl]User to reset the password connection errors:[{}]/[{}]'.format(
                    uid64, token
                )
            )
            return HttpResponse(
                u"Password reset failed!\nPassword reset link is invalid, possibly because it has been used. You can request a new password reset.",
                status=403
            )

    def changetx(self, request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]The user does not log in')
            raise PermissionDenied


        data = request.POST['tx']
        if not data:
            logger.error(
                u'[UserControl]Users upload an avatar is empty:[%s]'.format(
                    request.user.username
                )
            )
            return HttpResponse(u"Upload Avatar error", status=500)

        imgData = base64.b64decode(data)

        filename = "tx_100x100_{}.jpg".format(request.user.id)
        filedir = "sec_auth/static/tx/"
        static_root = getattr(settings, 'STATIC_ROOT', None)
        if static_root:
            filedir = os.path.join(static_root, 'tx')
        if not os.path.exists(filedir):
            os.makedirs(filedir)

        path = os.path.join(filedir, filename)

        file = open(path, "wb+")
        file.write(imgData)
        file.flush()
        file.close()


        im = Image.open(path)
        out = im.resize((100, 100), Image.ANTIALIAS)
        out.save(path)

   
        try:
            
            import qiniu

            qiniu_access_key = settings.QINIU_ACCESS_KEY
            qiniu_secret_key = settings.QINIU_SECRET_KEY
            qiniu_bucket_name = settings.QINIU_BUCKET_NAME

            assert qiniu_access_key and qiniu_secret_key and qiniu_bucket_name
            q = qiniu.Auth(qiniu_access_key, qiniu_secret_key)

            key = filename
            localfile = path

            mime_type = "text/plain"
            params = {'x:a': 'a'}

            token = q.upload_token(qiniu_bucket_name, key)
            ret, info = qiniu.put_file(token, key, localfile,
                                       mime_type=mime_type, check_crc=True)

           
            request.user.img = "http://{}/{}?v{}".format(
                settings.QINIU_URL,
                filename,
                time.strftime('%Y%m%d%H%M%S')
            )
            request.user.save()

            
            if ret['key'] != key or ret['hash'] != qiniu.etag(localfile):
                logger.error(
                    u'[UserControl]Upload Avatar error:[{}]'.format(
                        request.user.username
                    )
                )
                return HttpResponse(u"Upload Avatar error", status=500)

            return HttpResponse(u"Upload Avatar success!\n(Note that a 10-minute buffer)")

        except Exception as e:
            request.user.img = "/static/tx/"+filename
            request.user.save()

         
            if not os.path.exists(path):
                logger.error(
                    u'[UserControl]Error users to upload avatar:[{}]'.format(
                        request.user.username
                    )
                )
                return HttpResponse(u"Upload Avatar error", status=500)

            return HttpResponse(u"Upload Avatar success!\n(Note that a 10-minute buffer)")

    def notification(self, request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]The user does not log in')
            raise PermissionDenied

        notification_id = self.request.POST.get("notification_id", "")
        notification_id = int(notification_id)

        notification = Notification.objects.filter(
            pk=notification_id
        ).first()

        if notification:
            notification.is_read = True
            notification.save()
            mydict = {"url": notification.url}
            print(mydict)
        else:
            mydict = {"url": '#'}

        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )
