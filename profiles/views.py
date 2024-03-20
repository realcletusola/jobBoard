from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile,SavedJob,AppliedJob
from .serializers import UserProfileSerializer,SavedJobSerializer,AppliedJobSerializer
from listing.models import JobListing
from listing.serializers import JobListingSerializer

User = get_user_model()



# profile view begins

# user profile detail view 
class UserProfileDetailView(APIView):

    # get object method
    def get_object(self, pk):

        try:
            return UserProfile.objects.get(pk=pk)
        
        except UserProfile.DoesNotExist:
            raise Http404
        


    # get profile
    def get(self, request, pk):

        # get profile using the get_object method 
        obj = self.get_object(pk)

        # serialize data and return response
        serializer = UserProfileSerializer(obj)

        return Response({
            "success":"Profile fetched",
            "data":serializer.data,
            "status":status.HTTP_200_OK
        })
    


    # update profile with put method 
    def put(self, request, pk):
        # get current user
        user = self.request.user 
        user_email = user.email

        # update profile using the get_object method  
        obj = self.get_object(pk)

        # serialize data and return response
        serializer = UserProfileSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            # get new email from request data 
            new_email = serializer.validated_data["email"]
            # check if email exists
            chk_email = User.objects.filter(email__iexact=new_email)

            #check if new email is not current email and if new email already exists
            if new_email != user_email and chk_email.count():

                return Response({
                    "error":f"Email {new_email} already exists",
                    "status": status.HTTP_400_BAD_REQUEST
                })
            
            else:
                # update user email
                user.email = new_email
                user.save()

                # update profile
                serializer.save()

                return Response({
                    "success":"Profile updated",
                    "status": status.HTTP_201_CREATED
                })
            
        
        # return error if serializer is invalid 
        return Response({
            "error":"Bad request, please check the form and try again",
            "error_detail": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })



    # update profile with patch method 
    def patch(self, request, pk):
        # get current user
        user = self.request.user 
        user_email = user.email

        # update profile using the get_object method  
        obj = self.get_object(pk)

        # serialize data and return response
        serializer = UserProfileSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            # get new email from request data 
            new_email = serializer.validated_data["email"]
            # check if email exists
            chk_email = User.objects.filter(email__iexact=new_email)

            #check if new email is not current email and if new email already exists
            if new_email != user_email and chk_email.count():

                return Response({
                    "error":f"Email {new_email} already exists",
                    "status": status.HTTP_400_BAD_REQUEST
                })
            
            else:
                # update user email
                user.email = new_email
                user.save()

                # update profile
                serializer.save()

                return Response({
                    "success":"Profile updated",
                    "status": status.HTTP_201_CREATED
                })
            
        
        # retun error if serializer is invalid 
        return Response({
            "error":"Bad request, please check the form and try again",
            "error_detail": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })

# profile view ends 



# saved jobs view begins 

# get all saved jobs by current user    
class SavedJobListView(APIView):

    permission_classes = [IsAuthenticated]

    # get all jobs saved by user 
    def get(self, request):
        
        obj = SavedJob.objects.filter(user=self.request.user)
        serializer = SavedJobSerializer(obj, many=True)
        
        return Response({
            "success":"success",
            "data": serializer.data,
            "status": status.HTTP_200_OK
        })



# add to saved job 
# ajax can be used on the frontend to send addsavedjob request to prevent the page from reloading.
# post request should be sent together with the pk(id) from the job listing data
class AddSavedJobView(APIView):

    permission_classes = [IsAuthenticated]

    # add to saved jobs with pk 
    def post(self, request, pk):
        job_obj = JobListing.objects.get(pk=pk)

        # ensure job_obj exists
        if not job_obj:
            return Response({
                "error": "Job object does not exist",
                "status":status.HTTP_404_NOT_FOUND
            })
        
        # bind job_obj to data 
        data = request.data 
        data['job'] = job_obj

        # create serializer instance with data 
        serializer = SavedJobSerializer(data=data)

        # validate serializer 
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)

            return Response({
                "success":"Job saved",
                "status": status.HTTP_201_CREATED
            })
        
        # return error if serializer is invalid 
        return Response({
            "error":"Unable to save job",
            "error_detail":serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })



# saved job detail view 
class SavedJobDetailView(APIView):

    permission_classes = [IsAuthenticated]

    # get object 
    def get_object(self, pk):
        # filter queryset based on current user
        saved_job = SavedJob.objects.get(user=self.request.user, pk=pk)

        # get the object or return 404 error 

        # obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        job_obj = saved_job.job 
        queryset = JobListing.objects.get(pk=job_obj.pk)
        obj = get_object_or_404(queryset)

        return obj 
    

    # get saved job detail
    def get(self, request, pk):
        # get object using the get_object method 
        obj = self.get_object(pk)

        # serialize object and return response 
        serializer = JobListingSerializer(obj)

        return Response({
            "success": "Job fetched",
            "data": serializer.data, 
            "status": status.HTTP_200_OK
        })
    

    # delete saved job 
    def delete(self, request, pk):

        saved_job = SavedJob.objects.get(pk=pk)
        saved_job.delete()
        
        return Response({
            "success":"Job deleted",
            "status": status.HTTP_204_NO_CONTENT
        })


# saved jobs view ends  
    

# applied jobs view begins 
    
# get all applied jobs by current user    
class AppliedJobListView(APIView):

    permission_classes = [IsAuthenticated]

    # get all jobs saved by user 
    def get(self, request):
        
        obj = AppliedJob.objects.filter(user=self.request.user)
        serializer = AppliedJobSerializer(obj, many=True)
        
        return Response({
            "success":"success",
            "data": serializer.data,
            "status": status.HTTP_200_OK
        })



# applied job detail view 
class AppliedJobDetailView(APIView):

    permission_classes = [IsAuthenticated]

    # get object 
    def get_object(self, pk):
        # filter queryset based on current user
        applied_job = AppliedJob.objects.get(user=self.request.user, pk=pk)

        # get the object or return 404 error 

        # obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        job_obj = applied_job.job 
        queryset = JobListing.objects.get(pk=job_obj.pk)
        obj = get_object_or_404(queryset)

        return obj 
    

    # get saved job detail
    def get(self, request, pk):
        # get object using the get_object method 
        obj = self.get_object(pk)

        # serialize object and return response 
        serializer = JobListingSerializer(obj)

        return Response({
            "success": "Job fetched",
            "data": serializer.data, 
            "status": status.HTTP_200_OK
        })
    

    # delete saved job 
    def delete(self, request, pk):

        applied_job = AppliedJob.objects.get(pk=pk)
        applied_job.delete()
        
        return Response({
            "success":"Job deleted",
            "status": status.HTTP_204_NO_CONTENT
        })
    

# applied job view ends 
    
