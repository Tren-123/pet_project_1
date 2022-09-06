from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class Blogger(models.Model):
    """ Model representing a blogger info """
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    date_of_birth = models.DateField(blank=True, null=True, help_text="Enter your date of birth")
    short_bio = models.TextField(max_length=1000, blank=True, null=True, help_text="Enter your short bio")
    #Avatar field not completed. Should set sizes for storage images and directory for storage images.
    #It must be web sever or cloud(now it local dir), database storage only path to storage dir
    avatar = models.ImageField(upload_to="blog/images/avatars", blank=True, null=True, help_text="Upload your profile avatar")

    class Meta:
        verbose_name = "Blogger info"

    def __str__(self):
        """ String for representing the Model object. """
        return self.user.username

    def get_absolute_url(self):
        """ Return url to instance """
        return reverse('blogger', kwargs={'pk' : self.user_id})
    #TO FIX if both create user and add blogger info integrity error raised
    @receiver(post_save, sender=User)
    def create_user_blogger(sender, instance, created, **kwargs):
        if created:
            Blogger.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_blogger(sender, instance, **kwargs):
        instance.blogger.save()


class Blog_post(models.Model):
    """ Model representing blog posts related for bloggers """
    title = models.CharField(max_length=100, help_text="Enter a title that briefly reflects the essence of the post")
    content = models.TextField(help_text="Enter your text here")
    likes = models.ManyToManyField(User, related_name="blog_post_mm")
    dislikes = models.PositiveIntegerField(default=0)
    date_of_origin = models.DateTimeField(auto_now_add=True)
    date_of_update = models.DateTimeField(auto_now=True)
    blogger = models.ForeignKey(User, related_name= "blog_post", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        """ String for representing the Model object. """
        return f"{self.title}, {str(self.date_of_origin)[0:19]}"
    
    def get_absolute_url(self):
        """ Return url to instance """
        return reverse('post', kwargs={'pk' : self.id})
    
    def total_likes(self):
        """" Return amount of likes of post """
        return self.likes.count()