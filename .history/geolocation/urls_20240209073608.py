from django.urls import path
from .views import (
    earthquake_data,
    track_location,
    track_location_specific_location,
    get_current_user_weather,
    get_current_user_climate,
)

urlpatterns = [
    path("track-location/", track_location, name="track_location"),
    # path("earthquake-data/", EarthquakeData.as_view(), name="earthquake-data"),
    path("api/earthquake-data/", earthquake_data, name="earthquake-data"),
    path(
        "api/earthquake-data_specific/",
        track_location_specific_location,
        name="earthquake-data_specific",
    ),
    path(
        "api/user_weather_location/",
        get_current_user_weather,
        name="user_weather_location",
    ),
    path(
        "api/climate-base-on-user/",
        get_current_user_climate,
        name="climate-base-on-user",
    ),
]
