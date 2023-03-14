from django.urls import include, path
from .views import TestDataList


urlpatterns = [
    path('', TestDataList.as_view()),
]