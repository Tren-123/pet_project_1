from django import forms
from django.forms import ModelForm, TextInput
from .models import Blogger
from django.contrib.auth.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

class BloggerForm(ModelForm):
    class Meta:
        model = Blogger
        fields = ["date_of_birth", "short_bio"]