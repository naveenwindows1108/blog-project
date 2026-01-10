from django.urls import path
from . import views
from .views import logout, profile

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='blog-user-registration'),
    path('login/', views.LoginAPIView.as_view(), name='blog-login'),
    path('logout/', logout, name='blog-logout'),
    path('profile/', profile, name='blog-profile'),
]
