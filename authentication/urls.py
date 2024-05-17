from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('', show_auth, name='show_auth'),
    path('login', show_login, name='show_login'),
    path('api/login', auth_login, name='login'),
    path('register', show_register, name='show_register'),
    path('api/logout', auth_logout, name='logout'),
]