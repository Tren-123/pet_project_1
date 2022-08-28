from django.db import models
from datetime import date

# Create your models here.
class TestModel(models.Model):
    """Model for test purpose."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Blogger(models.Model):
    """Model for blogger info storage"""
    first_name = models.CharField(max_length=50, help_text='Enter your first name')
    second_name = models.CharField(max_length=50, help_text='Enter your second name')
    nickname = models.CharField(max_length=50, unique=True, blank=False, help_text='Enter unique nickname')
    e_mail = models.EmailField("E-mail", max_length=254, unique=True, blank=False, help_text='Enter your e-mail. Each e-mail can be registred only one time')
    date_of_bitrh = models.DateField(help_text="Enter your date of birth")
    short_bio = models.TextField(max_length=1000, help_text="Enter your short bio")
    avatar = models.ImageField(help_text="Upload your profile avatar")

    def __str__(self):
        """String for representing the Model object."""
        return self.name