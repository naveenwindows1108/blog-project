from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Post
from django.contrib.auth.models import User
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['GET'])
def home(request):
    if request.method == "GET":
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def about(request):
    return JsonResponse({'page': 'about'})

# Create your views here.
