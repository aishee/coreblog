# -*- coding: utf-8 -*-
from django import forms
from sec_auth.models import SecUser
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
import base64
import logging

logger = logging.getLogger(__name__)


#django.contrib.auth.forms.UserCreationForm
class SecUserCreationForm(forms.ModelForm):


    error_messages = {
        'duplicate_username': u"This user already exists.",
        'password_mismatch': u"The two passwords are not equal.",
        'duplicate_email': u'This email already exists.'
    }

    username = forms.RegexField(
        max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid':  u"This value must contain only letters, numbers and characters @/./+/-/_",
            'required': u"Username Unfilled"
        }
    )
    email = forms.EmailField(
        error_messages={
            'invalid':  u"Malformed email",
            'required': u'Email Unfilled'}
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': u"Password Unfilled"
            }
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': u"Confirm password Unfilled"
            }
    )

    class Meta:
        model = SecUser
        fields = ("username", "email")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            SecUser._default_manager.get(username=username)
        except SecUser.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages["duplicate_username"]
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                    self.error_messages["password_mismatch"]
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            SecUser._default_manager.get(email=email)
        except SecUser.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages["duplicate_email"]
        )

    def save(self, commit=True):
        user = super(SecUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SecPasswordRestForm(forms.Form):

    error_messages = {
        'email_error': u"This user does not exist or does not correspond to the user name and email.",
    }

    username = forms.RegexField(
        max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': u"This value must contain only letters, numbers and characters @/./+/-/_",
            'required': u"Username Unfilled"}
        )
    email = forms.EmailField(
        error_messages={
            'invalid':  u"Malformed email",
            'required': u'Email Unfilled'}
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username and email:
            try:
                self.user = SecUser.objects.get(
                    username=username, email=email, is_active=True
                )
            except SecUser.DoesNotExist:
                raise forms.ValidationError(
                    self.error_messages["email_error"]
                )

        return self.cleaned_data

    def save(self, from_email=None, request=None,
             token_generator=default_token_generator):
        email = self.cleaned_data['email']
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        uid = base64.urlsafe_b64encode(
            force_bytes(self.user.pk)
        ).rstrip(b'\n=')
        token = token_generator.make_token(self.user)
        protocol = 'http'

        title = u"Reset {} Password".format(site_name)
        message = "".join([
            u"You're receiving this letter because you request to reset your site {} Account password on\n\n".format(
                site_name
            ),
            u"Please visit this page and enter a new password:\n\n",
            "{}://{}/resetpassword/{}/{}/\n\n".format(
                protocol, domain, uid, token
            ),
            u"Your username, if you have forgotten the words:  {}\n\n".format(
                self.user.username
            ),
            u"Thank you for using our site!\n\n",
            u"{} Team\n\n\n".format(site_name)
        ])

        try:
            send_mail(title, message, from_email, [self.user.email])
        except Exception as e:
            logger.error(
                u'[UserControl]Mail failed to send the user to reset the password:[{}]/[{}]'.format(
                    username, email
                )
            )
