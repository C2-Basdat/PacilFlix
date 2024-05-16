from django.shortcuts import render

def index(request):
    return render(request, 'langganan.html', {})

def beli(request):
    return render(request, 'beli.html', {})