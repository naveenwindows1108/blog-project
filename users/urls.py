from django.urls import path
from . import views
from .views import logout

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(),
         name='blog-user-registration'),
    path('login/', views.LoginAPIView.as_view(), name='blog-login'),
    path('logout/', logout, name='blog-logout'),
    path('profiles/', views.GetProfilesAPIView.as_view(), name='blog-profile'),
    path('profiles/<int:pk>/', views.ProfileAPI.as_view(), name='user-profile')

]
