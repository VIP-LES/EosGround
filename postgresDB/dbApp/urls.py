from django.urls import include, path
from .views import PositionList, TelemetryList, TestDataList, TerminalOutputList, transmitTableInsert

# this is where we put the endpoint urls
# the postgresDB/urls.py file also has to be updated accordingly

urlpatterns = [
    path('pos/<int:pk>/', PositionList.as_view(), name='retrieve-position'),
    path('tel/<int:pk>/', TelemetryList.as_view(), name='retrieve-telemetry'),
    path('test/<int:pk>/', TestDataList.as_view(), name='retrieve-testdata'),
    path('terminal/', TerminalOutputList.as_view(), name='terminal-output'),
    path('insertTransmitTable/', transmitTableInsert, name='transmit-table-insert')
]
