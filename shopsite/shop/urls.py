from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('author/', views.author_page, name='author'),
    path('store/', views.store_page, name='store'),
]