from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import json
import time
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


# class EarthquakeData(APIView):
#     def get_earthquake_data(
#         self,
#         starttime,
#         endtime,
#         minmagnitude=5,
#         latitude=None,
#         longitude=None,
#         maxradiuskm=None,
#     ):
#         base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
#         params = {
#             "format": "geojson",
#             "starttime": starttime,
#             "endtime": endtime,
#             "minmagnitude": minmagnitude,
#             "latitude": latitude,
#             "longitude": longitude,
#             "maxradiuskm": maxradiuskm,
#         }

#         response = requests.get(base_url, params=params)

#         if response.status_code == 200:
#             return response.json().get("features", [])
#         else:
#             print(f"Error {response.status_code}: {response.text}")
#             return None

#     def get_location_data(self):
#         ip = requests.get("https://api.ipify.org?format=json")
#         ip_data = json.loads(ip.text)
#         res = requests.get("http://ip-api.com/json/" + ip_data["ip"])
#         location_data = res.text

#         main_location = json.loads(location_data)

#         return main_location.get("lat"), main_location.get("lon")

#     def get(self, request):
#         # Get user's location data
#         latitude, longitude = self.get_location_data()

#         # Get earthquake data for the last X minutes (adjust as needed)
#         end_time = time.strftime("%Y-%m-%dT%H:%M:%S")
#         start_time = (time.strptime(end_time, "%Y-%m-%dT%H:%M:%S").tm_sec - 5 * 60) % 60
#         start_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(start_time))

#         earthquake_data = self.get_earthquake_data(
#             start_time,
#             end_time,
#             latitude=latitude,
#             longitude=longitude,
#             maxradiuskm=100,  # Adjust the radius as needed
#         )

#         # Process and save the retrieved data
#         if earthquake_data:
#             for quake in earthquake_data:
#                 properties = quake.get("properties", {})
#                 Earthquake.objects.create(
#                     place=properties.get("place"),
#                     time=properties.get("time"),
#                     magnitude=properties.get("mag"),
#                     latitude=quake.get("geometry", {}).get("coordinates", [])[1],
#                     longitude=quake.get("geometry", {}).get("coordinates", [])[0],
#                 )
#             serializer = EarthquakeSerializer(Earthquake.objects.all(), many=True)
#             return Response(serializer.data)
#         else:
#             return Response(
#                 {"detail": "No earthquake data retrieved for the last 5 minutes."}
#             )


# class EarthquakeData(APIView):
#     def get_earthquake_data(
#         self, latitude, longitude, minmagnitude=5, maxradiuskm=None
#     ):
#         base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
#         params = {
#             "format": "geojson",
#             "latitude": latitude,
#             "longitude": longitude,
#             "minmagnitude": minmagnitude,
#             "maxradiuskm": maxradiuskm,
#         }

#         response = requests.get(base_url, params=params)

#         if response.status_code == 200:
#             return response.json().get("features", [])
#         else:
#             print(f"Error {response.status_code}: {response.text}")
#             return None

#     def get_location_data(self):
#         ip = requests.get("https://api.ipify.org?format=json")
#         ip_data = json.loads(ip.text)
#         res = requests.get("http://ip-api.com/json/" + ip_data["ip"])
#         location_data = res.text

#         main_location = json.loads(location_data)

#         return main_location.get("lat"), main_location.get("lon")

#     def get(self, request):
#         # Get user's location data
#         latitude, longitude = self.get_location_data()

#         # Get earthquake data for the user's location at the current moment
#         earthquake_data = self.get_earthquake_data(
#             latitude=latitude,
#             longitude=longitude,
#             maxradiuskm=100,  # Adjust the radius as needed
#         )

#         # Process and save the retrieved data
#         if earthquake_data:
#             for quake in earthquake_data:
#                 properties = quake.get("properties", {})
#                 Earthquake.objects.create(
#                     place=properties.get("place"),
#                     time=properties.get("time"),
#                     magnitude=properties.get("mag"),
#                     latitude=quake.get("geometry", {}).get("coordinates", [])[1],
#                     longitude=quake.get("geometry", {}).get("coordinates", [])[0],
#                 )
#             serializer = EarthquakeSerializer(Earthquake.objects.all(), many=True)
#             return Response(serializer.data)
#         else:
#             return Response(
#                 {
#                     "detail": "No earthquake data available for the user's location at the moment."
#                 }
#             )


# class EarthquakeData(APIView):
#     def get_earthquake_data(
#         self, latitude, longitude, minmagnitude=5, maxradiuskm=None
#     ):
#         base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
#         params = {
#             "format": "geojson",
#             "latitude": latitude,
#             "longitude": longitude,
#             "minmagnitude": minmagnitude,
#             "maxradiuskm": maxradiuskm,
#         }

#         response = requests.get(base_url, params=params)

#         if response.status_code == 200:
#             return response.json().get("features", [])
#         else:
#             print(f"Error {response.status_code}: {response.text}")
#             return None

#     def get(self, request):
#         # For testing purposes, let's use a fixed location (e.g., San Francisco, CA)
#         fixed_latitude = 34.0522
#         fixed_longitude = -118.2437

#         # Get earthquake data for the fixed location at the current moment
#         earthquake_data = self.get_earthquake_data(
#             latitude=fixed_latitude,
#             longitude=fixed_longitude,
#             maxradiuskm=100,  # Adjust the radius as needed
#         )

#         # Process and save the retrieved data
#         if earthquake_data:
#             for quake in earthquake_data:
#                 properties = quake.get("properties", {})
#                 Earthquake.objects.create(
#                     place=properties.get("place"),
#                     time=properties.get("time"),
#                     magnitude=properties.get("mag"),
#                     latitude=quake.get("geometry", {}).get("coordinates", [])[1],
#                     longitude=quake.get("geometry", {}).get("coordinates", [])[0],
#                 )
#             serializer = EarthquakeSerializer(Earthquake.objects.all(), many=True)
#             return Response(serializer.data)
#         else:
#             return Response(
#                 {
#                     "detail": "No earthquake data available for the specified location at the moment."
#                 }
#             )


class EarthquakeData(APIView):
    def get_earthquake_data(self, latitude, longitude):
        base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = {
            "format": "geojson",
            "latitude": latitude,
            "longitude": longitude,
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            return response.json().get("features", [])
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def get(self, request):
        # For testing purposes, let's use a fixed location (e.g., San Francisco, CA)
        fixed_latitude = 34.0522
        fixed_longitude = -118.2437

        # Get all earthquake data for the fixed location
        earthquake_data = self.get_earthquake_data(
            latitude=fixed_latitude,
            longitude=fixed_longitude,
        )

        # Process and save the retrieved data
        if earthquake_data:
            for quake in earthquake_data:
                properties = quake.get("properties", {})
                Earthquake.objects.create(
                    place=properties.get("place"),
                    time=properties.get("time"),
                    magnitude=properties.get("mag"),
                    latitude=quake.get("geometry", {}).get("coordinates", [])[1],
                    longitude=quake.get("geometry", {}).get("coordinates", [])[0],
                )
            serializer = EarthquakeSerializer(Earthquake.objects.all(), many=True)
            return Response(serializer.data)
        else:
            return Response(
                {
                    "detail": "No earthquake data available for the specified location in the past."
                }
            )
