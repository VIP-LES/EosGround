# Create your views here.
from .models import TestData
from .serializers import TestDataSerializer
from rest_framework import generics
class TestDataList(generics.RetrieveAPIView):
    # API endpoint that allows data to be viewed.
    queryset = TestData.objects.all()
    serializer_class = TestDataSerializer

