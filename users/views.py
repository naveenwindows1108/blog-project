from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.contrib.auth.password_validation import validate_password
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from . models import Profile
from django.db import transaction
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .handlers import error_message, success_message
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from .utility.jwt_auth import jwt_required, jwt_token


def register(request):
    if request.method != 'POST':
        return error_message('Not a valid method', 405)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return error_message('Json syntax error')
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')

    if not username or not password or not phone:
        return error_message('all fields are required')
    try:
        validate_password(password)
    except ValidationError as e:
        return error_message(e.messages)
    if User.objects.filter(username=username).exists():
        return error_message('user already exists')
    if Profile.objects.filter(phone=phone).exists():
        return error_message('phone already exists')
    try:
        with transaction.atomic():
            user = User.objects.create_user(
                username=username, password=password)
            Profile.objects.create(user=user, phone=phone)
    except Exception as e:
        print(f'ERROR: {e}')
        return error_message('Registration failed', 500)

    return success_message(data={'user_id': user.id, 'username': user.username}, message=f'{user.username} created successfully', status_code=201)


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return error_message('Not a valid method', 405)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return error_message('syntax error in json')

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return error_message('all fields are required')
    user = authenticate(username=username, password=password)
    if user is None:
        return error_message('invalid credentials', 401)
    token = jwt_token(user)
    return success_message(data={'user_id': user.id, 'username': user.username, 'token': token}, message='logged in successfully', status_code=200)


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


def getcsrf(request):
    if request.method == 'GET':
        return JsonResponse({
            'csrf_token': get_token(request)
        })
