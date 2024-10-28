from django.conf import settings
from django.core.mail import send_mail

def send_account_activation_email(email, email_token):
    try:
        subject = "Verify your email id to continue"
        message = f"Click the link to verify your email id http://127.0.0.1:8000/verify/{email_token}/{email}"
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[email])
    except Exception as e:
        print(e)