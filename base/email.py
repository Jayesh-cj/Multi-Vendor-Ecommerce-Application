from django.conf import settings
from django.core.mail import send_mail

def send_account_activation_email(email, email_token):
    try:
        pass
    except Exception as e:
        print(e)