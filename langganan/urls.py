from django.urls import path

from . import views

app_name = 'langganan'

urlpatterns = [
    path('', views.index, name='index'),
    path('beli/', views.beli, name='beli')
]