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
    """
    Get earthquake data based on specified parameters.

    Parameters:
    - `starttime` (optional): Start time for earthquake search (default is "2017-01-01T00:00:00").
    - `endtime` (optional): End time for earthquake search (default is the current time).
    - `minmagnitude` (optional): Minimum magnitude of earthquakes to retrieve (default is 5).
    - `format` (optional): Format of the earthquake data (default is "geojson").
    - `latitude` (optional): Latitude of the location.
    - `longitude` (optional): Longitude of the location.
    - `maxradiuskm` (optional): Maximum radius in kilometers for earthquake search.
    - `limit` (optional): Limit the number of earthquakes to retrieve (default is 20).

    Returns:
    List of dictionaries containing earthquake information.

    Example Response:
    [
        {
            "place": "Reykjanes Ridge",
            "date": "2024-02-07 07:52:04",
            "magnitude": 5
        },
        {
            "place": "175 km SSW of Abepura, Indonesia",
            "date": "2024-02-07 07:52:10",
            "magnitude": 5
        },
        ...
    ]
    """

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
    """
    Get location information and earthquake data based on the user's IP address.

    Returns:
    - `location`: Dictionary containing relevant location information.
    - `earthquake_data`: List of dictionaries containing earthquake information.

    Example Response:
    {
        "location": {
            "status": "success",
            "country": "Cameroon",
            "countryCode": "CM",
            "region": "NW",
            "regionName": "North-West Region",
            "city": "Bamenda"
        },
        "earthquake_data": [
            {
                "place": "Reykjanes Ridge",
                "date": "2024-02-07 07:52:04",
                "magnitude": 5
            },
            {
                "place": "175 km SSW of Abepura, Indonesia",
                "date": "2024-02-07 07:52:10",
                "magnitude": 5
            },
            ...
        ]
    }
    """
    ip = requests.get("https://api.ipify.org?format=json")
    ip_data = json.loads(ip.text)
    res = requests.get("http://ip-api.com/json/" + ip_data["ip"])
    location_data = json.loads(res.text)

    # Extract relevant information from the location data
    relevant_location_data = {
        "status": location_data.get("status"),
        "country": location_data.get("country"),
        "countryCode": location_data.get("countryCode"),
        "region": location_data.get("region"),
        "regionName": location_data.get("regionName"),
        "city": location_data.get("city"),
    }

    # Extract latitude and longitude from the location data
    latitude = location_data.get("lat")
    longitude = location_data.get("lon")

    # Use the latitude and longitude to fetch earthquake data
    earthquake_data = get_earthquake_data(latitude, longitude)

    return Response(
        {"location": relevant_location_data, "earthquake_data": earthquake_data}
    )


def get_earthquake_data(
    latitude, longitude, minmagnitude=5, format="geojson", maxradiuskm=100, limit=20
):
    """
    Get earthquake data based on the specified latitude and longitude.

    Args:
    - `latitude`: Latitude of the location.
    - `longitude`: Longitude of the location.
    - `minmagnitude`: Minimum magnitude of earthquakes to retrieve (default is 5).
    - `format`: Format of the earthquake data (default is 'geojson').
    - `maxradiuskm`: Maximum radius in kilometers for earthquake search (default is 100).
    - `limit`: Limit the number of earthquakes to retrieve (default is 20).

    Returns:
    - List of dictionaries containing earthquake information.

    Example Response:
    [
        {
            "place": "Reykjanes Ridge",
            "date": "2024-02-07 07:52:04",
            "magnitude": 5
        },
        {
            "place": "175 km SSW of Abepura, Indonesia",
            "date": "2024-02-07 07:52:10",
            "magnitude": 5
        },
        ...
    ]
    """
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
