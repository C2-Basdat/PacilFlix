from django.shortcuts import render

def show_auth(request):
    return render(request, 'auth.html')

def show_login(request):
    return render(request, 'login.html')

def show_register(request):
    return render(request, 'register.html')
