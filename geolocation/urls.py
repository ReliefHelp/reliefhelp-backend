from django.urls import path
from .views import track_location

urlpatterns = [
    path('track-location/', track_location, name='track_location'),
]