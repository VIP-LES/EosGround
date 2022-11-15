from django.shortcuts import render

# Create your views here.
from dbApp.models import RawData
from django.views import View

class DataTable(View):
    def get_data(self, request):
        allData = RawData.objects.all()
        for data in allData:
            print(data.packet_type)
            print(data.priority)
            print(data.device)
            print(data.body)
            print()

        return render(request, 'rawdata.html')
