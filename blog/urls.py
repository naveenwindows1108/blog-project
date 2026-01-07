from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomeAPI.as_view(), name='blog-home'),
    path('post/<int:pk>/', views.HomePostAPI.as_view(), name='blog-about'),
]
