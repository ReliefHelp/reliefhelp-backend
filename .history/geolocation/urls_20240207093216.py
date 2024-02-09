from django.urls import path
from .views import earthquake_data, track_location, track_location_specific_location

urlpatterns = [
    path("track-location/", track_location, name="track_location"),
    # path("earthquake-data/", EarthquakeData.as_view(), name="earthquake-data"),
    path("api/earthquake-data/", earthquake_data, name="earthquake-data"),
    path(
        "api/earthquake-data_specific/",
        track_location_specific_location,
        name="earthquake-data_specific",
    ),
]
