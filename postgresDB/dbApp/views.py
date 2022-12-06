from django.shortcuts import render

# Create your views here.
from dbApp.models import RawData
from django.views import View

""" def get_all_devices(request):
    #get list of all devices
    all_dev_list = list(RawData.objects.values('packet_sender'))
    context = {
        "dev_list": all_dev_list,
    }
    #return render(request, "data_tables.html", context)
    #uncomment when data_tables html is done  """

def device_info(request):
    #get info from specific device - pass in device #
    #all_dev_list = list(RawData.objects.values('packet_sender'))
    #device_info = RawData.objects.get(pk=pk)

    raw_data = RawData.objects.order_by('packet_sender')

    context = {
        #"dev_list": all_dev_list,
        #"dev_info": device_info
        "raw_data": raw_data,
    }
    return render(request, "data_tables.html", context)
