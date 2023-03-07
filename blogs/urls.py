from django.urls import path
import django.contrib.auth.views as auth_views
from . import views

app_name = 'blogs'
urlpatterns = [
    path('', views.blogs, name='index'),
    path('<slug:slug>/', views.blog_details, name='details'),
]
