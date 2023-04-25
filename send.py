import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.mail import send_mail

send_mail(
    'Subject here',
    'Here is the message.',
    'tommoway228@gmail.com',
    ['tommoway228@gmail.com'],
    fail_silently=False,
)
