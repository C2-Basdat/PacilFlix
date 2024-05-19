from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('daftar-favorit/', include('daftar_favorit.urls')),
    path('daftar-unduhan/', include('daftar_unduhan.urls')),
    path('langganan/', include('langganan.urls')),
    path('kontributor/', include('kontributor.urls')),
    path('fakhri-hijau/', include('fakhri_hijau.urls')),
    path('auth/', include('authentication.urls')),
    path('', RedirectView.as_view(url='/fakhri-hijau/tayangan', permanent=False)),
]