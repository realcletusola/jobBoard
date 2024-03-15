from rest_framework import serializers 
from django.contrib.auth import get_user_model

import re 


User = get_user_model()



# Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password_again = serializers.CharField(required=True)


    class Meta:
        model = User
        fields = ('email','password','password_again')


    # validate email 
    def validate_email(self, value):
        # perform custome validation on email field 
        if value is None:
            raise serializers.ValidationError("Email is required")
        if len(value) < 8 or len(value) > 60:
            raise serializers.ValidationError("Email must be between 8 to 60 characters only")
        
        return value 
    
    # validate passwords  
    def validate(self, data):
        # perform custom validation on password fields  
        password = data.get("password")
        password_again = data.get("password_again")

        if password is None or password_again is None:
            raise serializers.ValidationError("Password fields are required")
        
        if len(password) < 8 or len(password_again) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        
        if not re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$", password):
            raise serializers.ValidationError("Password must contain at least one uppercase, lowercase, digit and special character")

        if password and password_again and password != password_again:
            raise serializers.ValidationError("Passwords must match")  

        return data      

    # create user 
    def create(self, validated_data):

        email = validated_data["email"]
        password = validated_data["password"]
        
        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()

        return user


# Login serializer 
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=8, max_length=60, required=True)
    password = serializers.CharField(min_length=8, required=True)

    