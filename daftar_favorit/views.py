from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required(login_url = '/login')
def show_daftar_favorit(request):
    daftar_favorit_user = []
        
    context = {
        'daftar_favorit_user': daftar_favorit_user
    }
    return render(request, 'daftar_favorit.html', context)

def show_daftar_favorit_tw(request):
    daftar_favorit_user = [
        {
            'timestamp': '2024-03-30 03:49:25',
            'judul': 'The Dark Knight'
        },
        {
            'timestamp': '2024-03-12 07:26:15',
            'judul': 'Interstellar'
        },
        {
            'timestamp': '2024-03-08 15:39:43',
            'judul': 'Inception'
        },
        {
            'timestamp': '2024-04-30 21:16:00',
            'judul': 'La La Land'
        },
        {
            'timestamp': '2024-03-24 08:11:14',
            'judul': 'Narcos'
        },
        {
            'timestamp': '2024-03-30 09:48:57',
            'judul': 'Avengers: Endgame'
        },
        {
            'timestamp': '2024-03-15 02:56:13',
            'judul': 'Sherlock Holmes'
        },
        {
            'timestamp': '2024-03-06 19:00:07',
            'judul': 'The Lord of the Rings'
        },
    ]
        
    context = {
        'daftar_favorit_user': daftar_favorit_user
    }
    return render(request, 'daftar_favorit_tailwind.html', context)
