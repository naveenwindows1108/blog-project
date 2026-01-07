from django.urls import path
from . import views
from .views import register
from .views import login, logout, getcsrf, profile

urlpatterns = [
    path('register/', views.register, name='blog-user-registration'),
    path('login/', login, name='blog-login'),
    path('logout/', logout, name='blog-logout'),
    path('register/', register, name='blog-register'),
    path('profile/', profile, name='blog-profile'),
    path('getcsrf/', getcsrf, name='csrf-token'),
]
