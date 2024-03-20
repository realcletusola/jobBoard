from rest_framework import serializers 

from .models import JobListing


# Job Listing serializer 
class JobListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobListing
        fields = ['id','title','company','description','company_mail','date_posted','deadline']




# Job application serializer 
class JobApplicationSerializer(serializers.Serializer):
    user = serializers.CharField(required=False)
    resume = serializers.FileField(required=True)
    cover_letter_file = serializers.FileField(required=False)
    cover_letter_text = serializers.TextField(required=False)

