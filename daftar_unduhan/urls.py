from django.urls import path
from daftar_unduhan.views import show_daftar_unduhan

app_name = 'daftar_unduhan'

urlpatterns = [
    path('', show_daftar_unduhan, name='show_daftar_unduhan'),
]