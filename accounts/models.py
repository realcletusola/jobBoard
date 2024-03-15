from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)


# custom user manager  
class CustomUserManager(BaseUserManager):

    # function to create user 
    def create_user(self, email, password, **extra_fields):

        if email is None:
            raise ValueError(_("Email is required"))
        
        email = self.normalize_email(email)
        user = self.model(email=email)

        if password is None:
            raise ValueError(_("Password is required"))
        
        user.is_active = True 
        user.is_staff = False 
        user.is_superuser = False
        user.set_password(password)
        user.save()

        return user 
    

    # function to create superuser 
    def create_superuser(self, email, password, **extra_fields):

        if email is None:
            raise ValueError(_("Email is required"))
        
        email = self.normalize_email(email)
        user = self.model(email=email)

        if password is None:
            raise ValueError(_("Password is required"))
        
        user.is_active = True 
        user.is_staff = True 
        user.is_superuser = True
        user.set_password(password)
        user.save()

        return user 

        
# user model 
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email 