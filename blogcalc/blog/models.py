from pyexpat import model
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
    date_of_origin = models.DateTimeField(auto_now_add=True)
    date_of_update = models.DateTimeField(auto_now=True)
    blogger = models.ForeignKey(User, related_name= "blog_post", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        """ String for representing the Model object. """
        return f"{self.title}, {str(self.date_of_origin)[0:19]}"
    
    def get_absolute_url(self):
        """ Return url to instance """
        return reverse('post', kwargs={'pk' : self.id})


class Likes_dislikes(models.Model):
    """ Model representing like/dislike reaction of specific user to specific post """
    blogger = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    blog_post = models.ForeignKey(Blog_post, on_delete=models.CASCADE)
    dislike = -1
    nothing = 0
    like = 1
    likes_dislike_choises = [
        (dislike, "Dislike"),
        (nothing, "No reaction"),
        (like, "Like"),
    ]
    like_dislike = models.SmallIntegerField(choices=likes_dislike_choises, default=0)

    def __str__(self):
        """ String for representing the Model object. """
        return f"{self.blog_post}, {self.blogger}, {self.get_like_dislike_display()}"