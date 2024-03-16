from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import JobListing
from .serializers import JobListingSerializer
from .mixins import RedisCacheMixin 



# Job List View
class JobListView(RedisCacheMixin, ListAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer


# Job Detail View 
class JobDetailView(RedisCacheMixin, RetrieveAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer

