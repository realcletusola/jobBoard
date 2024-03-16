from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer
from .tasks import send_signup_mail


# Registration View 
class UserRegistrationView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_signup_mail.delay(user.email) # trigger celery send mail function 

            return Response({
                "message": f"Account created for {user.email} successfully",
                "status":status.HTTP_201_CREATED
            })


# Login View 
class UserLoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(email=email, password=password)

            if user is not None:

                if user.is_active:
                    refresh = RefreshToken.for_user(user)

                    return Response({
                        "message":f"You're successfully logged in as {user.email}",
                        "refresh_token":str(refresh),
                        "access_token":str(refresh.access_token),
                        "status":status.HTTP_200_OK
                    })
                
                else:
                    return Response({
                        "error":"Your account is inactive",
                        "status": status.HTTP_401_UNAUTHORIZED
                    })
            
            else:
                return Response({
                    "message":"Incorrect email or password",
                    "status": status.HTTP_401_UNAUTHORIZED
                })
            
        return Response({
            "error":serializer.errors,
            "status":status.HTTP_400_BAD_REQUEST
        })


# Logout View 
class UserLogoutView(APIView):

    def post(self, request):

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "message":"You're logged out successfully",
                "status": status.HTTP_205_RESET_CONTENT
            })
        
        except Exception as e:
            return Response({
                "error": str(e),
                "status": status.HTTP_400_BAD_REQUEST
            })
            

