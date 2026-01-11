from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as django_logout
from .handlers import error_message, success_message
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .utility.jwt_auth import jwt_required
from .serializers import UserRegisterSerializer
from .serializers import ListProfilesSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        return Response(data={
            'message': 'user created successfully',
            'user_id': user.id,
            'email': user.email,
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        return Response(data={
            'message': 'Login Successful',
            'user_id': user.id,
            'email': user.username

        }, status=status.HTTP_200_OK)


@csrf_exempt
def logout(request):

    if request.method != 'POST':
        return error_message('POST method required', 405)

    if not request.user.is_authenticated:
        return error_message('user not logged in', 401)

    django_logout(request)
    return success_message(message=' logOut successfully')


# @jwt_required
# def profile(request):
#     if request.method != 'GET':
#         return error_message(message='use GET method only', status_code=405)
#     if not request.user.is_authenticated:
#         return error_message('login first to fetch profile', 401)
#     user = request.user
#     return success_message(data={'user': user.username}, message='Profile fetched successfully', status_code=200)


class GetProfilesAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = ListProfilesSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileAPI(APIView):
    def get_user_object(self, pk):
        return get_object_or_404(User, id=pk)

    def get(self, request, pk):
        user = self.get_user_object(pk=pk)
        serializer = ListProfilesSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def put(self, request, pk):
    #     new_data=request.data
    #     serializer = ListProfilesSerializer(self.get_user_object(pk=pk))
    #     return Response(serializer.data, status=status.HTTP_200_OK)
