#-*- coding: utf-8 -*-
from models import *

from django import template
from django import forms
from django.utils.translation import ugettext_lazy as _


class UserPasswordForm(forms.Form):
    old_password = forms.CharField(label=u'Stare hasło', required=True, widget=forms.PasswordInput)
    new_password = forms.CharField(label=u'Nowe hasło', required=True, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=u'Nowe hasło', required=True, widget=forms.PasswordInput)