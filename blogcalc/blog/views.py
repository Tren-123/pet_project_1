from django.shortcuts import render
from .models import Blogger, Blog_post
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    """View functions of index page of site"""
    last_5_blogger = User.objects.all()
    last_5_blog_posts = Blog_post.objects.all()
    
    context = {
        'last_5_blogger': last_5_blogger,
        'last_5_blog_posts': last_5_blog_posts,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)