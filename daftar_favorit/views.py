from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required(login_url = '/login')
def show_daftar_favorit(request):
    daftar_favorit_user = []
        
    context = {
        'daftar_favorit_user': daftar_favorit_user
    }
    return render(request, 'daftar_favorit.html', context)