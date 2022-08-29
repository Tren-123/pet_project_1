from distutils.command.upload import upload
from email.utils import localtime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blogger(models.Model):
    """Model representing a blogger info"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    date_of_bitrh = models.DateField(blank=True, null=True, help_text="Enter your date of birth")
    short_bio = models.TextField(max_length=1000, blank=True, null=True, help_text="Enter your short bio")
    #Avatar field not completed. Should set sizes for storage images and directory for storage images.
    #It must be web sever or cloud(now it local dir), database storage only path to storage dir
    avatar = models.ImageField(upload_to="blog/images/avatars", blank=True, null=True, help_text="Upload your profile avatar")

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username

class Blog_post(models.Model):
    """Model representing blog posts related for bloggers"""
    title = models.CharField(max_length=100, help_text="Enter a title that briefly reflects the essence of the post")
    content = models.TextField(help_text="Enter your text here")
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    date_of_origin = models.DateTimeField(auto_now=True)
    blogger = models.ForeignKey(Blogger, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.title}, {str(self.date_of_origin)[0:19]}"