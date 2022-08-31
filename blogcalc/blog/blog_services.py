from .models import Blog_post
from django.contrib.auth.models import User


def get_query_with_new_n_bloggers(n : int):
    """ return query of n new bloggers """
    return User.objects.filter(is_staff = 0).order_by("-date_joined")[: n]
 
def get_query_with_new_n_blog_posts(n : int):
    return Blog_post.objects.all().order_by("-date_of_origin")[: n]