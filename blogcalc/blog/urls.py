from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bloggers/", views.BloggerListView.as_view(), name="bloggers"),
    path("posts/", views.Blog_postListView.as_view(), name="posts"),
    path("blogger/<int:pk>", views.BloggerDetailView.as_view(), name="blogger"),
    path("post/<int:pk>", views.BlogPostDetailView.as_view(), name="post"),
    path("like/<int:pk>", views.LikeView, name="like_post"),
    path("dislike/<int:pk>", views.DislikeView, name="dislike_post"),
    path("post/create", views.BlogPostCreate.as_view(), name="create_post"),
    path("blogger/<int:pk>/update", views.BloggerUpdate.as_view(), name="blogger_update"),
    path("blogger/create", views.NewUserCreate, name="create_blogger"),
    path("post/<int:pk>/new_comment/<int:blogger_id>", views.NewComment, name="post_new_comment"),
    path("post/<int:pk>/delete", views.BlogPostDeleteView.as_view(), name="post_delete"),
    path("blogger/<int:pk>/delete", views.BloggerDeleteView.as_view(), name="blogger_delete"),
    ]