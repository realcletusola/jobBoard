from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import JobListing
from .serializers import JobListingSerializer, JobApplicationSerializer
from .mixins import RedisCacheMixin 
from profiles.models import AppliedJob 
from accounts.tasks import send_application_mail, send_application_confirmation_mail

User = get_user_model()


# Job List View
class JobListView(RedisCacheMixin, ListAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer


# Job Detail View 
class JobDetailView(RedisCacheMixin, RetrieveAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer


# job application view  
class JobApplicationView(APIView):

    permission_classes = [IsAuthenticated]

    # post request for job applicaion 
    def post(self, request, pk):
        # get current user and user email 
        user = self.request.user 
        user_email = self.request.user.email 

        # get job object 
        job = JobListing.objects.get(pk=pk)
        job_mail = job.company_mail

        # ensure job exist
        if not job:
            return Response({
                "error": "Job not found",
                "status": status.HTTP_404_NOT_FOUND
            })
        
        # job serializer
        serializer = JobApplicationSerializer(data=request.data)

        # validate serializer data 
        if serializer.is_valid(raise_exception=True):

            # give both cover letters initial value of none
            # the user should be allowed to either upload a cover letter file or type in a cover letter in a text box
            cover_letter_file = None 
            cover_letter_text = None

            # get resume from submitted data 
            resume = serializer.validated_data["resume"]
            
            # if cover letter was provided in file format
            if serializer.validated_data["cover_letter_file"]:
                cover_letter_file = serializer.validated_data["cover_letter_file"]
            
            # else cover letter was provided in text format
            elif serializer.validated_data["cover_letter_text"]:
                cover_letter_text = serializer.validated_data["cover_letter_text"]

            else:
                pass 

            # set email details 
            subject = f"New job application {job.title} position"
            sender_email = settings.EMAIL_HOST_USER
            receiver_email = job_mail
            # give email body an initial value of none
            body = None

            # if cover_letter_text is not none
            if cover_letter_text is not None and cover_letter_file is None:
                body = f""" You've received a new job application form {user_email} for the {job.title} position. \n 
                        Applicant cover letter:\n {cover_letter_text}\n Attached to this mail is the cv of the applicant."""

                # call celery task asynchronously 
                try:
                    send_application_mail.delay(subject,body,sender_email,receiver_email,resume, user, job)
                   
                    # send application email confirmation
                    try:
                        send_application_confirmation_mail.delay(subject, body, sender_email, user_email)
                    
                    # allow application continue even if confirmation email is not sent, since it will be saved in the applied job model
                    except:
                        pass 
                    return Response({
                        "success":"Application sent",
                        "status": status.HTTP_200_OK
                    })
                
                except:
                    return Response({
                        "error":"Something went wrong, please try again later.",
                        "status": status.HTTP_400_BAD_REQUEST
                    })
                

            # if cover_letter_file is not none
            if cover_letter_file is not None and cover_letter_text is None:
                body = f""" You've received a new job application form {user_email} for the {job.title} position. \n 
                        Attached to this mail is the resume and cover letter of the applicant. """

                # call celery task asynchronously 
                try:
                    # send application email
                    send_application_mail.delay(subject,body,sender_email,receiver_email,resume, user, job, cover_letter_file)
                    
                    # send application email confirmation
                    try:
                        send_application_confirmation_mail.delay(subject, body, sender_email, user_email)
                    
                    # allow application continue even if confirmation email is not sent, since it will be saved in the applied job model
                    except:
                        pass 


                    return Response({
                        "success":"Application sent",
                        "status": status.HTTP_200_OK
                    })
                
                except:
                    return Response({
                        "error":"Something went wrong, please try again later.",
                        "status": status.HTTP_400_BAD_REQUEST
                    })

        

