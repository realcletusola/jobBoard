from rest_framework import serializers 

from .models import JobListing


# Job Listing serializer 
class JobListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobListing
        fields = ['id','title','company','description','date_posted','deadline']


      