from .models import Post
from .serializers import PostSerializer
from rest_framework import generics

class HomeAPI(generics.ListAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer


class HomePostAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    



