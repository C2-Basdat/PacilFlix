from django.urls import path
from fakhri_hijau.views import *


urlpatterns = [
    path('trailer', read_trailer, name='read_trailer'),
    path('tayangan', read_tayangan, name='read_tayangan'),
    path('film-series/<str:id_tayangan>', read_film_series, name='read_film_series'),
]