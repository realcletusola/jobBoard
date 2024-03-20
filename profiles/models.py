from django.db import models
from django.contrib.auth import get_user_model

from listing.models import JobListing

User = get_user_model()


# User Profile Model  
class UserProfile(models.Model):
    full_name = models.CharField(max_length=40, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=60, blank=True, null=True)
    phone = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.user 


# Saved Jobs Model
class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_job")
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.job 
    
# Applied Jobs Model 
class AppliedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applied_job")
    job = models.ForeignKey(JobListing, on_delete=models.DO_NOTHING, related_name="applied")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.job 
    
    
