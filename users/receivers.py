from django.dispatch import receiver
from .signals import read_signal


@receiver(read_signal)
def handle_user_visit(sender, date_time, **kwargs):
    if date_time:
        print(f'Home api visited at {date_time}')
