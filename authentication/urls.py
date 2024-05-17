from django.urls import path
from authentication.views import show_auth, show_login, show_register

app_name = 'authentication'

urlpatterns = [
    path('', show_auth, name='show_auth'),
    path('login', show_login, name='show_login'),
    path('register', show_register, name='show_register')
]