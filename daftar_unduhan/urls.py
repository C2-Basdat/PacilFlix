from django.urls import path
from daftar_unduhan.views import show_daftar_unduhan, show_daftar_unduhan_tw

app_name = 'daftar_unduhan'

urlpatterns = [
    path('', show_daftar_unduhan, name='show_daftar_unduhan'),
    path('tw', show_daftar_unduhan_tw, name='show_daftar_unduhan_tw'),
]