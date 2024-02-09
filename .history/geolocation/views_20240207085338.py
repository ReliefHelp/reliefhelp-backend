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


# class EarthquakeData(APIView):
#     def get_earthquake_data(
#         self,
#         start_time,
#         end_time,
#         min_magnitude=5,
#         format="geojson",
#         latitude=None,
#         longitude=None,
#         max_radius_km=None,
#     ):
#         base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
#         params = {
#             "format": format,
#             "starttime": start_time,
#             "endtime": end_time,
#             "minmagnitude": min_magnitude,
#             "latitude": latitude,
#             "longitude": longitude,
#             "maxradiuskm": max_radius_km,
#         }

#         response = requests.get(base_url, params=params)

#         if response.status_code == 200:
#             return response.json()
#         else:
#             print(f"Error {response.status_code}: {response.text}")
#             return None

#     def get(self, request):
#         # Specify the location (e.g., San Francisco, CA)
#         specified_latitude = 37.7749
#         specified_longitude = -122.4194

#         # Set the time range (adjust as needed)
#         end_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
#         start_time = (datetime.utcnow() - timedelta(minutes=5)).strftime(
#             "%Y-%m-%dT%H:%M:%S"
#         )

#         # Get earthquake data for the specified location and time range
#         earthquake_data = self.get_earthquake_data(
#             start_time=start_time,
#             end_time=end_time,
#             latitude=specified_latitude,
#             longitude=specified_longitude,
#             max_radius_km=10000,  # Adjust the radius as needed
#         )


#         # Process and save the retrieved data
#         if earthquake_data:
#             features = earthquake_data.get("features", [])
#             if features:
#                 for quake in features:
#                     properties = quake.get("properties", {})
#                     print(
#                         f"Earthquake at {properties['place']} on {properties['time']} with magnitude {properties['mag']}"
#                     )
#                 return Response(features)
#             else:
#                 print("No earthquake features found.")
#                 return Response(
#                     {
#                         "detail": "No earthquake features found for the specified location and time range."
#                     }
#                 )
#         else:
#             print("No earthquake data retrieved.")
#             return Response(
#                 {
#                     "detail": "No earthquake data available for the specified location and time range."
#                 }
#             )
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
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    # Get request parameters
    interval_minutes = int(request.query_params.get("interval_minutes", 5))
    num_updates = int(request.query_params.get("num_updates", 5))
    latitude = request.query_params.get("latitude")
    longitude = request.query_params.get("longitude")
    maxradiuskm = request.query_params.get("maxradiuskm")

    earthquake_results = []

    for _ in range(num_updates):
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=interval_minutes)

        start_time_str = start_time.isoformat()
        end_time_str = end_time.isoformat()

        print(f"Start Time: {start_time_str}, End Time: {end_time_str}")

        earthquake_data = get_earthquake_data(
            start_time_str,
            end_time_str,
            latitude=latitude,
            longitude=longitude,
            maxradiuskm=maxradiuskm,
        )

        print(f"Earthquake Data: {earthquake_data}")

        # Process the retrieved data
        if earthquake_data:
            features = earthquake_data.get("features", [])
            for quake in features:
                properties = quake.get("properties", {})
                earthquake_results.append(
                    {
                        "place": properties["place"],
                        "time": properties["time"],
                        "magnitude": properties["mag"],
                    }
                )

    return Response(earthquake_results)
