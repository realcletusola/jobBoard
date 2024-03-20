from django.urls import path 

from .views import (
    UserProfileDetailView,
    SavedJobListView,
    SavedJobDetailView,
    AddSavedJobView,
    AppliedJobListView,
    AppliedJobDetailView
)


urlpatterns = [
    path('/<int:pk>/', UserProfileDetailView.as_view(), name='profile_detail'),
    path('savedjobs/', SavedJobListView.as_view(), name='saved_jobs'),
    path('savedjobs/<int:pk>/', SavedJobDetailView.as_view(), name='saved_job_details'),
    path('addsavedjob/<int:pk>/', AddSavedJobView.as_view(), name='add_saved_jobs'),
    path('appliedjobs/', AppliedJobListView.as_view(), name='applied_jobs'),
    path('applied_job/<int:pk>/', AppliedJobDetailView.as_view(), name='applied_job_details'),
]

