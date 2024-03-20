from celery import shared_task 
from django.core.mail import send_mail, EmailMessage
from django.conf import settings 

from profiles.models import AppliedJob


# task to send email on signup 
@shared_task(autoretry_for=(Exception, ), max_retries=3) # retry for 3 times if task fails on first try
def send_signup_mail(user_email):
    
    subject = "Welcome to JobBoard"
    message = "Thank you for signing up on JobBoard."
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)


# task to send job application email 
@shared_task(autoretry_for=(Exception, ), max_retries=3) # retry 3 times if task fails on first try
def send_application_mail(subject, body, sender_email, receiver_email, resume, user, job, cover_letter_file=None):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=sender_email,
        to=[receiver_email],
    )

    # attach resume 
    email.attach[resume]

    # check if cover letter file is not none
    if cover_letter_file is not None:
        email.attach_file[cover_letter_file]
    else:
        pass 

    email.send()

    # save applied job to AppliedJob models
    AppliedJob.objects.create(
        user=user,
        job=job
    )


# task to send job application confirmation email 
@shared_task(autoretry_for=(Exception, ), max_retries=3)
def send_application_confirmation_mail(subject, body, sender_email, reciever_email):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=sender_email,
        to=[reciever_email]
    )

    email.send()