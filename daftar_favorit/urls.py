from django.urls import path
from daftar_favorit.views import show_daftar_favorit, show_daftar_favorit_tw

app_name = 'daftar_favorit'

urlpatterns = [
    path('', show_daftar_favorit, name='show_daftar_favorit'),
    path('tw', show_daftar_favorit_tw, name='show_daftar_favorit_tw')
]