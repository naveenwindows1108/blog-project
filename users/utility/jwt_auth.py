import jwt
from django.contrib.auth.models import User
import datetime
from functools import wraps
from ..handlers import error_message
from django_project.settings import SECRET_KEY
ALGORITHM = "HS256"


def jwt_token(user):
    if not user or not user.is_authenticated:
        return None
    payload = {
        "username": user.username,
        "exp": datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=15),
        'iat': datetime.datetime.now(datetime.timezone.utc)

    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def jwt_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return error_message(message='Header is missing', status_code=401)
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.user = User.objects.get(username=payload['username'])
        except jwt.ExpiredSignatureError:
            return error_message(message='Token is expired, please re-login', status_code=401)
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return error_message(message='Invalid token or user is not logged in', status_code=401)
        return func(request, *args, **kwargs)
    return wrapper
