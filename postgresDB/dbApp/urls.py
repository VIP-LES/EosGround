from django.urls import include, path
from .views import TestDataList


urlpatterns = [
    path('<int:pk>/', TestDataList.as_view(), name='retrieve-data'),
]