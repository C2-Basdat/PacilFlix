from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required(login_url='/login')
def show_daftar_unduhan(request):
    context = {}
    return render(request, 'daftar_unduhan.html', context)