from rest_framework import serializers
from .models import TestData


class TestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestData
        fields = ['pk', 'packet', 'random_int']