from django.shortcuts import render
from nara_backend.models import Traffic
from rest_framework import viewsets
from nara_backend.serializers import TrafficSerializer
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# class TrafficViewSet(viewsets.ModelViewSet):
    # """ API Endopint """
    # queryset = Traffic.objects.all().order_by('-created_date')
    # serializer_class = TrafficSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def traffic_list(request):
    if request.method == 'GET':
        traffic = Traffic.objects.all()
        serializer = TrafficSerializer(traffic, many=True)
        return JSONResponse(serializer.data)


