from django.contrib import admin

from .models import JobListing


# Job Listing admin 
class JobListingAdmin(admin.ModelAdmin):
    list_display = ["title","company","date_posted","deadline"]
    list_display_links = ["title","company"]
    