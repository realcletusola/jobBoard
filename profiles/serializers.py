from rest_framework import serializers 

from .models import UserProfile, SavedJob, AppliedJob 


# User Profile serializer 
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id','full_name','email','phone']


# Saved Job serializer 
class SavedJobSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False) # user field return a string and not an object
    job = serializers.CharField(required=False) # user field return a string and not an object

    class Meta:
        model = SavedJob
        fields = ['id','user','job','date']

# Applied Job serializer 
class AppliedJobSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False) # user field return a string and not an object
    job = serializers.CharField(required=False) # user field return a string and not an object

    class Meta:
        model = AppliedJob
        fields = ['id','user','job','date']
