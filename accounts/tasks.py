from celery import shared_task 
from django.core.mail import send_mail
from django.conf import settings 


# task to send email on signup 
@shared_task(autoretry_for=(Exception, ), max_retries=3) # retry for up to 3 times if there's any error
def send_signup_mail(user_email):
    
    subject = "Welcome to JobBoard"
    message = "Thank you for signing up on JobBoard."
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)

