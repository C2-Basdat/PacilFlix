from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('beli/', views.beli, name='beli')
]