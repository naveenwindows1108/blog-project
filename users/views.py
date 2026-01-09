from django.contrib.auth.models import User
import json
from django.contrib.auth.password_validation import validate_password
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth import logout as django_logout
from .handlers import error_message, success_message
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .utility.jwt_auth import jwt_required

@csrf_exempt
def register(request):
    if request.method != 'POST':
        return error_message('Not a valid method', 405)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return error_message('Json syntax error')
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return error_message('all fields are required')
    try:
        validate_password(password)
    except ValidationError as e:
        return error_message(e.messages)
    if User.objects.filter(email=email).exists():
        return error_message('user already exists')
    user = User.objects.create_user(username=email, password=password)

    return success_message(data={'user_id': user.id, 'email': user.username}, message=f'{user.username} created successfully', status_code=201)


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


@jwt_required
def profile(request):
    if request.method != 'GET':
        return error_message(message='use GET method only', status_code=405)
    if not request.user.is_authenticated:
        return error_message('login first to fetch profile', 401)
    user = request.user
    return success_message(data={'user': user.username}, message='Profile fetched successfully', status_code=200)


# def getcsrf(request):
#     if request.method == 'GET':
#         return JsonResponse({
#             'csrf_token': get_token(request)
#         })
