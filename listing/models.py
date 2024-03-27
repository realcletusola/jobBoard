from django.db import models
 

# Job Listing Model
class JobListing(models.Model):
    title = models.CharField(max_length=30, blank=False, null=False)
    company = models.CharField(max_length=30, blank=False, null=False)
    description = models.TextField()
    company_mail = models.EmailField(max_length=60, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']
        
    def __str__(self):
        return self.title 
