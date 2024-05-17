from django.urls import path
from fakhri_hijau.views import *


urlpatterns = [
    path('trailer', read_trailer, name='read_trailer'),
    path('tayangan', read_tayangan, name='read_tayangan'),
    path('episode', read_episode, name='read_episode'),
    path('ulasan', create_read_ulasan, name='create_read_ulasan'),
    path('film-series/<str:id_tayangan>', read_film_series, name='read_film_series'),
    path('download-tayangan/<str:id_tayangan>', download_tayangan, name='download_tayangan'),
]