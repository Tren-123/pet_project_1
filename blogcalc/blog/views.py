from django.shortcuts import render
from .blog_services import get_query_with_new_n_bloggers, \
                         get_query_with_new_n_blog_posts, \
                         get_query_for_all_bloggers
from django.views import generic
from django.contrib.auth.models import User


def index(request):
    """View functions of index page of site"""
    last_n_blogger = get_query_with_new_n_bloggers(5)
    last_n_blog_posts = get_query_with_new_n_blog_posts(5)

    context = {
        'last_n_blogger': last_n_blogger,
        'last_n_blog_posts': last_n_blog_posts,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BloggerListView(generic.ListView):
    model = User
    template_name = "bloggers_list.html"
    queryset = get_query_for_all_bloggers()
    paginate_by = 10
    