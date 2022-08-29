from distutils.command.upload import upload
from email.utils import localtime
from django.db import models
import time
from datetime import datetime

# Create your models here.

class Blogger(models.Model):
    """Model representing a blogger info"""
    first_name = models.CharField(max_length=50, blank=True, null=True, help_text='Enter your first name')
    second_name = models.CharField(max_length=50, blank=True, null=True, help_text='Enter your second name')
    nickname = models.CharField(max_length=50, unique=True, blank=False, help_text='Enter unique nickname')
    e_mail = models.EmailField("E-mail", unique=True, blank=False, help_text="Enter your e-mail. Each e-mail can be registred only one time")
    date_of_bitrh = models.DateField(blank=True, null=True, help_text="Enter your date of birth")
    short_bio = models.TextField(max_length=1000, blank=True, null=True, help_text="Enter your short bio")
    #Avatar field not completed. Should set sizes for storage images and directory for storage images.
    #It must be web sever or cloud(now it local dir), database storage only path to storage dir
    avatar = models.ImageField(upload_to="blog/images/avatars", blank=True, null=True, help_text="Upload your profile avatar")

    def __str__(self):
        """String for representing the Model object."""
        return self.nickname

class Blog_post(models.Model):
    """Model representing blog posts related for bloggers"""
    title = models.CharField(max_length=100, help_text="Enter a title that briefly reflects the essence of the post")
    content = models.TextField(help_text="Enter your text here")
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    date_of_origin = datetime(*time.localtime()[0:6]) 
    blogger = models.ForeignKey(Blogger, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.title}, {self.date_of_origin}"