from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bloggers/", views.BloggerListView.as_view(), name="bloggers"),
    path("posts/", views.Blog_postListView.as_view(), name="posts"),
    path("blogger/<int:pk>", views.BloggerDetailView.as_view(), name="blogger"),
    ]