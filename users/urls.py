from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter,SimpleRouter

router = DefaultRouter()
router.register('profiles', views.UsersViewset, basename='profile')
urlpatterns = router.urls
# urlpatterns = [
#     path('register/', views.RegisterAPIView.as_view(),
#          name='blog-user-registration'),
#     path('login/', views.LoginAPIView.as_view(), name='blog-login'),
#     path('profiles/', views.ProfilesAPIView.as_view(), name='blog-profile'),
#     path('profile/<int:pk>/', views.ProfileAPIView.as_view(), name='user-profile')

# ]
