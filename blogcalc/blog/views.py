from django.shortcuts import render
from .blog_services import get_query_with_new_n_bloggers, \
                         get_query_with_new_n_blog_posts, \
                         get_query_for_all_bloggers, \
                         get_query_for_all_posts
from django.views import generic
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User
from .models import Blog_post


def index(request):
    """View functions of index page of site"""
    last_n_blogger = get_query_with_new_n_bloggers(n=5)
    last_n_blog_posts = get_query_with_new_n_blog_posts(n=5)

    context = {
        'last_n_blogger': last_n_blogger,
        'last_n_blog_posts': last_n_blog_posts,
    }
    return render(request, 'index.html', context=context)

class BloggerListView(generic.ListView):
    model = User
    template_name = "bloggers_list.html"
    queryset = get_query_for_all_bloggers()
    paginate_by = 10
    
class Blog_postListView(generic.ListView):
    model = Blog_post
    template_name = "blog_post_list.html"
    queryset = get_query_for_all_posts()
    paginate_by = 10

class BloggerDetailView(generic.DetailView, MultipleObjectMixin):
    model = User
    template_name = "blogger_detail_view.html"
    def get_context_data(self, **kwargs):
        object_list = Blog_post.objects.filter(blogger_id=self.get_object().id)
        context = super(BloggerDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context
    paginate_by = 10

class BlogPostDetailView(generic.DetailView):
    model = Blog_post
    template_name = "blog_post_detail_view.html"