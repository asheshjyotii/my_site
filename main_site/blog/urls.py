from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts_page'),
    path('posts/<slug:slug>/', views.particular_post, name='particular_post_page'),
]