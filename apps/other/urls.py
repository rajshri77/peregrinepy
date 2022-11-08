from django.urls import path
from apps.other.views import GetVolume

urlpatterns = [
    path('get/volume', GetVolume.as_view(), name='get_volume')
]
