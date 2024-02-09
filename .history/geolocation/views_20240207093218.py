from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import json
import time
from datetime import datetime, timedelta

from geolocation.models import Earthquake

from geolocation.serializer import EarthquakeSerializer

@api_view(['GET'])
def track_location(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
    location_data = res.text

    main_location = json.loads(location_data)

    return Response(main_location)


@api_view()
def earthquake_data(request):
    def get_earthquake_data(
        starttime,
        endtime,
        minmagnitude=5,
        format="geojson",
        latitude=None,
        longitude=None,
        maxradiuskm=None,
        limit=20,
    ):
        base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = {
            "format": format,
            "starttime": starttime,
            "endtime": endtime,
            "minmagnitude": minmagnitude,
            "latitude": latitude,
            "longitude": longitude,
            "maxradiuskm": maxradiuskm,
            "limit": limit,
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    # Get request parameters
    starttime = request.query_params.get("starttime", "2017-01-01T00:00:00")
    endtime = request.query_params.get(
        "endtime", datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    )
    minmagnitude = request.query_params.get("minmagnitude", 5)
    latitude = request.query_params.get("latitude")
    longitude = request.query_params.get("longitude")
    maxradiuskm = request.query_params.get("maxradiuskm")
    limit = request.query_params.get("limit", 20)

    earthquake_results = []

    # Retrieve earthquake data
    earthquake_data = get_earthquake_data(
        starttime,
        endtime,
        minmagnitude=minmagnitude,
        format="geojson",
        latitude=latitude,
        longitude=longitude,
        maxradiuskm=maxradiuskm,
        limit=limit,
    )

    # Process the retrieved data
    if earthquake_data:
        features = earthquake_data.get("features", [])
        for quake in features:
            properties = quake.get("properties", {})
            date_time = datetime.utcfromtimestamp(properties["time"] / 1000.0).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            earthquake_results.append(
                {
                    "place": properties["place"],
                    "date": date_time,
                    "magnitude": properties["mag"],
                }
            )

    return Response(earthquake_results)


@api_view(["GET"])
def track_location_specific_location(request):
    ip = requests.get("https://api.ipify.org?format=json")
    ip_data = json.loads(ip.text)
    res = requests.get("http://ip-api.com/json/" + ip_data["ip"])
    location_data = res.text

    main_location = json.loads(location_data)

    # Extract latitude and longitude from the location data
    latitude = main_location["lat"]
    longitude = main_location["lon"]

    # Use the latitude and longitude to fetch earthquake data
    earthquake_data = get_earthquake_data(latitude, longitude)

    return Response({"location": main_location, "earthquake_data": earthquake_data})


def get_earthquake_data(
    latitude, longitude, minmagnitude=5, format="geojson", maxradiuskm=100, limit=20
):
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": format,
        "latitude": latitude,
        "longitude": longitude,
        "minmagnitude": minmagnitude,
        "maxradiuskm": maxradiuskm,
        "limit": limit,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        earthquake_data = response.json()
        features = earthquake_data.get("features", [])
        result = []

        for quake in features:
            properties = quake.get("properties", {})
            date_time = datetime.utcfromtimestamp(properties["time"] / 1000.0).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            result.append(
                {
                    "place": properties["place"],
                    "date": date_time,
                    "magnitude": properties["mag"],
                }
            )

        return result
    else:
        return None
