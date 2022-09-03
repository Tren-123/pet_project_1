from django.db import models

# Create your models here.
class Calculator(models.Model):
    title = models.CharField(max_length=200)
    context = models.CharField(max_length=1500)


    def __str__(self):
        return self.title