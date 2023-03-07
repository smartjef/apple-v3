from django.urls import path
from . import views

app_name = 'root'
urlpatterns = [
    path('', views.index, name='index'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.advanced_search, name='search'),
]
