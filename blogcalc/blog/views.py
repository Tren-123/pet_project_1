from re import A
from django.shortcuts import render, get_object_or_404
from .blog_services import get_query_with_new_n_bloggers, \
                         get_query_with_new_n_blog_posts, \
                         get_query_for_all_bloggers, \
                         get_query_for_all_posts, \
                         get_total_like, get_total_dislike, \
                         get_all_comments_for_blog_post   
                        
from django.views import generic
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User
from .models import Blog_post, Blogger, Likes_dislikes, Comment
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import UserForm, BloggerForm, CreateUserForm
from django.contrib.auth import authenticate, login
from django import forms


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
    context_object_name = "blogger"
    def get_context_data(self, **kwargs):
        object_list = Blog_post.objects.filter(blogger_id=self.get_object().id).order_by("-date_of_origin")
        context = super(BloggerDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context
    paginate_by = 10

class BlogPostDetailView(generic.DetailView, MultipleObjectMixin):
    model = Blog_post
    template_name = "blog_post_detail_view.html"
    def get_context_data(self, **kwargs):
        object_list = get_all_comments_for_blog_post(self.object.id)
        context = super(BlogPostDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context["total_likes"] = get_total_like(self.object.id)
        context["total_dislikes"] = get_total_dislike(self.object.id)
        return context


def LikeView(request, pk):
    if request.user.is_authenticated:
        obj, created = Likes_dislikes.objects.get_or_create(blog_post_id = request.POST.get("post_id"),
                                                            blogger_id = request.user.id,
                                                            )
        if obj.like_dislike == 0:
            obj.like_dislike = 1
        else:
            obj.like_dislike = 0
        obj.save(update_fields=["like_dislike"])
    return HttpResponseRedirect(reverse("post", args=[str(pk)]))

def DislikeView(request, pk):
    if request.user.is_authenticated:
        obj, created = Likes_dislikes.objects.get_or_create(blog_post_id = request.POST.get("post_id"),
                                                            blogger_id = request.user.id,
                                                            )
        if obj.like_dislike == 0:
            obj.like_dislike = -1
        else:
            obj.like_dislike = 0
        obj.save(update_fields=["like_dislike"])
    return HttpResponseRedirect(reverse("post", args=[str(pk)]))

class BlogPostCreate(LoginRequiredMixin, CreateView):
    model = Blog_post
    template_name = "blog_post_create_view.html"
    fields = ["title", "content"]
    def form_valid(self, form):
        form.instance.blogger = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(BlogPostCreate, self).get_form(form_class)
        form.fields['title'].widget = forms.TextInput(attrs={'autocomplete': 'off'})
        return form
    
class BloggerUpdate(LoginRequiredMixin, generic.TemplateView):
    template_name = "blogger_update_view.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        context["user_form"] = UserForm(instance=user)
        context["blogger_form"] = BloggerForm(instance=user.blogger)
        return context

    def post(self, request, *args, **kwargs):
        # retrieve the User model instance based on authenticated user id
        user = self.request.user
        # create a UserForm based on user and form data
        user_form = UserForm(instance=user, data=request.POST)
        # retrieve the Blogger model instance based on authenticated user id
        blogger = get_object_or_404(Blogger, user_id=self.request.user.id)
        # create a BloggerForm based on blogger and form data
        blogger_form = BloggerForm(instance=blogger, data=request.POST, files=request.FILES)
        # if the save_user button is pressed
        if 'save_user_info' in request.POST:
            if user_form.is_bound and user_form.is_valid():
                user_form.save()
                return HttpResponseRedirect(reverse('blogger_update', kwargs={'pk': self.request.user.id}))
        
        # if the save_blogger_info button is pressed
        elif 'save_blogger_info' in request.POST:
            if blogger_form.is_bound and blogger_form.is_valid():
                blogger_form.save()
                return HttpResponseRedirect(reverse('blogger_update', kwargs={'pk': self.request.user.id}))

        # if the return_to_blogger_view button is pressed
        elif "return_to_blogger_view" in request.POST:       
            return HttpResponseRedirect(reverse('blogger', kwargs={'pk': self.request.user.id}))


def NewUserCreate(request, *args, **kwargs):
    #TO DO add tests for credentials
    if request.method == 'POST' and "save" in request.POST:
        form = CreateUserForm(request.POST)
        new_user_username = form["username"].value()
        new_user_password1 = form["password1"].value()
        new_user_password2 = form["password2"].value()
        if form.is_valid():
            if new_user_password1 == new_user_password2:
                user = User.objects.create_user(username=new_user_username, password=new_user_password1)
                login(request, user)
                return HttpResponseRedirect(reverse('blogger_update', kwargs={'pk': user.id}))
    else:
        form = CreateUserForm()
    return render(request, 'blogger_create_view.html', {'form': form})


def NewComment(request, pk, blogger_id):
    if request.user.is_authenticated:
        new_comment = Comment(content=request.POST.get("comment_text"), blog_post_id = pk, blogger_id = blogger_id)
        new_comment.save()
    return HttpResponseRedirect(reverse("post", args=[str(pk)]))

class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog_post
    template_name = "blog_post_delete_view.html"
    def get_success_url(self):
        return reverse('blogger', kwargs={'pk': self.object.blogger_id})
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.blogger_id != self.request.user.id:
            raise Http404("You are not allowed to delete this Post")
        return super(BlogPostDeleteView, self).dispatch(request, *args, **kwargs)