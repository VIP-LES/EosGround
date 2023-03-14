# Create your views here.
from django.views import View
from django.shortcuts import render
from .models import TestData
from rest_framework import generics
from .serializers import TestDataSerializer

class TestDataList(generics.ListAPIView):
    # API endpoint that allows data to be viewed.
    queryset = TestData.objects.all()
    serializer_class = TestDataSerializer

