from django.urls import include, path
from .views import PositionList, TelemetryList

urlpatterns = [
    path('pos/<int:pk>/', PositionList.as_view(), name='retrieve-position'),
    path('tel/<int:pk>/', TelemetryList.as_view(), name='retrieve-telemetry'),
]