from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import UserProfile 

User = get_user_model()


# signal to create user profile on sign up
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)


# save user profile 
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()