import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import psycopg2
from authentication.backends import AuthBackend
from django.views.decorators.csrf import csrf_exempt

def show_auth(request):
    return render(request, 'auth.html')

def show_login(request):
    return render(request, 'login.html')

def show_register(request):
    return render(request, 'register.html')

@csrf_exempt
def auth_login(request):
    if request.method == 'POST':
        be = AuthBackend()
        requestBody = json.load(request)
        username = requestBody['username']
        password = requestBody['password']
        user = be.authenticate(username, password)
        if user is not None:
            be.login(request, user)
            return JsonResponse({'message': 'Login success!'}, status=200)
        else:
            return JsonResponse({'message': 'Login failed! Wrong username or password.'}, status=401)

@csrf_exempt
def auth_logout(request):
    if request.method == 'POST':
        be = AuthBackend()
        be.logout(request)
        return HttpResponse("OK")
    
@csrf_exempt
def auth_register(request):
    if request.method == 'POST':
        requestBody = json.load(request)
        username = requestBody['username']
        password = requestBody['password']
        negara_asal = requestBody['negara_asal']
        be = AuthBackend()
        result = be.register(username, password, negara_asal)
        if isinstance(result, psycopg2.errors.RaiseException):
            return JsonResponse({'message': 'Register fail!'}, status=401)
        else:
            return JsonResponse({'message': 'Register success!'}, status=200)