from django.http import JsonResponse


def error_message(message, status_code=400):
    return JsonResponse({
        'message': message
    }, status=status_code)


def success_message(data=None, message=None, status_code=200):
    return JsonResponse({
        'message': message,
        'data': data
    }, status=status_code)
