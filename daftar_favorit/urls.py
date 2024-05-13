from django.urls import path
from daftar_favorit.views import show_daftar_favorit

app_name = 'daftar_favorit'

urlpatterns = [
    path('', show_daftar_favorit, name='show_daftar_favorit')
]