from .models import Blog_post, Blogger, Likes_dislikes, Comment
from django.contrib.auth.models import User


def get_query_with_new_n_bloggers(n : int):
    """ return query of n new bloggers """
    return User.objects.filter(is_staff = 0).order_by("-date_joined")[: n]
 
def get_query_with_new_n_blog_posts(n : int):
    """ return query of n new bloggers posts """
    return Blog_post.objects.all().order_by("-date_of_origin")[: n]

def get_query_for_all_bloggers():
    """ return query of all bloggers """
    return User.objects.filter(is_staff = 0).order_by("username")

def get_query_for_all_posts():
    """ return query of all posts """
    return Blog_post.objects.all().order_by("-date_of_origin")

def get_total_like(id_of_post):
    """ return total likes from specific user for specific post  """
    return Likes_dislikes.objects.filter(blog_post_id = id_of_post, like_dislike = 1).count()

def get_total_dislike(id_of_post):
    """ return total dislikes from specific user for specific post  """
    return Likes_dislikes.objects.filter(blog_post_id = id_of_post, like_dislike = -1).count()

def get_all_comments_for_blog_post(id_of_post):
    """ return all comments to blog_post with id id_of_post """
    return Comment.objects.filter(blog_post_id = id_of_post).order_by("date_of_origin")