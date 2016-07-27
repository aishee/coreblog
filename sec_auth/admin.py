# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from sec_auth.models import SecUser
from sec_auth.forms import SecUserCreationForm


# Register your models here.

class SecUserAdmin(UserAdmin):
    add_form = SecUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )
    fieldsets = (
        (u'Basic Information', {'fields': ('username', 'password', 'email')}),
        (u'Competence', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (u'Time information', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.unregister(Group)
admin.site.register(SecUser, SecUserAdmin)
