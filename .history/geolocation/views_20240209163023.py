from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
import requests
import json
import time
from datetime import datetime, timedelta
from geolocation.models import Earthquake

from geolocation.serializer import EarthquakeSerializer
from dotenv import load_dotenv
import os

load_dotenv()

@api_view(['GET'])
def track_location(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
    location_data = res.text

    main_location = json.loads(location_data)

    return Response(main_location)


@api_view()
@permission_classes([IsAuthenticated])
def earthquake_data(request):
    """
    Get earthquake data based on specified parameters.
    Parameters
    - starttime (str): The start time for the earthquake data retrieval in the format 'YYYY-MM-DDTHH:MM:SS'.
    - endtime (str): The end time for the earthquake data retrieval in the format 'YYYY-MM-DDTHH:MM:SS'.
    - minmagnitude (float): The minimum magnitude of earthquakes to include in the results.
    - format (str): The format of the response data (default is 'geojson').
    - latitude (float): The latitude of the location for earthquake data retrieval.
    - longitude (float): The longitude of the location for earthquake data retrieval.
    - maxradiuskm (float): The maximum radius (in kilometers) from the specified location for data retrieval.
    - limit (int): The maximum number of earthquakes to retrieve (default is 20).
    Returns
    A list of dictionaries containing earthquake information with keys:
    - place (str): The location of the earthquake.
    - date (str): The date and time of the earthquake in 'YYYY-MM-DD HH:MM:SS' format.
    - magnitude (float): The magnitude of the earthquake.
    Example
    ```
    GET /earthquake-data/?starttime=2022-01-01T00:00:00&endtime=2022-02-01T00:00:00&latitude=37.7749&longitude=-122.4194
    This will retrieve earthquake data for the specified time range and location.
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
@permission_classes([IsAuthenticated])
def track_location_specific_location(request):
    """
    Get location information and earthquake data based on the user's IP address.
    Returns
    - `location`: Dictionary containing relevant location information.
    - `earthquake_data`: List of dictionaries containing earthquake information.
    Example Response
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_weather(request):
    """
    API endpoint to retrieve current weather data for the user's location
    Parameters
    None
    Returns
    Response JSON response containing weather data or an error message.
    """

    # Fetch the user's IP address
    ip = requests.get("https://api.ipify.org?format=json")
    ip_data = json.loads(ip.text)

    # Get location details using the IP address
    res = requests.get("http://ip-api.com/json/" + ip_data["ip"])
    location_data = json.loads(res.text)

    def get_weather_data(api_key, latitude, longitude):
        """
        Helper function to fetch weather data from the OpenWeatherMap API.
        Parameters
        api_key (str): OpenWeatherMap API key.
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

        Returns:
        dict: Dictionary containing weather data.
        """
        base_url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": api_key,
        }
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            weather = {
                "name": data.get("name"),
                "weather_state": data.get("weather", []),
            }
            return weather

    # OpenWeatherMap API key
    api_key = os.environ.get("api_key")

    # Get user's current location details
    latitude = location_data.get("lat")
    longitude = location_data.get("lon")

    # Get current weather data
    weather_data = get_weather_data(api_key, latitude, longitude)

    if weather_data:
        return Response({"weather_data": weather_data})
    else:
        return Response({"detail": "Weather data not found"}, status=404)
