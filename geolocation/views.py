from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json

@api_view(['GET'])
def track_location(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
    location_data = res.text

    main_location = json.loads(location_data)

    return Response(main_location)