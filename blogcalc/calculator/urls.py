from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='visualizer-index'),
    path('data', views.pivot_data, name='pivot_data')
]