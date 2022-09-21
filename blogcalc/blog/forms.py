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
        fields = ["date_of_birth", "short_bio", "avatar"]


class CreateUserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150, help_text=" Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. ")
    password1 = forms.CharField(label="Password", max_length=150, widget=forms.PasswordInput,help_text="<ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>")
    password2 = forms.CharField(label="Password confirmation", max_length=150, widget=forms.PasswordInput,)