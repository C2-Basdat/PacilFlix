from django.urls import path
from daftar_favorit.views import delete_daftar_favorit, show_daftar_favorit, add_daftar_favorit

app_name = 'daftar_favorit'

urlpatterns = [
    path('', show_daftar_favorit, name='show_daftar_favorit'),
    path('add-daftar-favorit/<str:judul>', add_daftar_favorit, name='add_daftar_favorit'),
    path('delete-daftar-favorit/<str:judul>', delete_daftar_favorit, name='delete_daftar_favorit')
]