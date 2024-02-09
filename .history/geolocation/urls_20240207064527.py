from django.urls import path
from .views import EarthquakeData, track_location

urlpatterns = [
    path("track-location/", track_location, name="track_location"),
    path("earthquake-data/", EarthquakeData.as_view(), name="earthquake-data"),
]
