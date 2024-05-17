from datetime import datetime
from django.shortcuts import redirect, render

from utils import DatabaseConnection

def show_daftar_unduhan(request):
    # verify login
    if request.session['user'] == None:
        return redirect("/auth")
    context = {'authenticated' : True, 'user' : request.session['user']}

    username = request.session['user']['username']
    select_query = f"SELECT timestamp, judul FROM TAYANGAN_TERUNDUH TT JOIN TAYANGAN T ON TT.id_tayangan = T.id WHERE TT.username = '{username}'"

    database = DatabaseConnection()
    daftar_unduhan = database.query(select_query)

    context['daftar_unduhan'] = daftar_unduhan

    return render(request, 'daftar_unduhan.html', context)

def add_daftar_unduhan(request, id_tayangan):
    # verify login
    if request.session['user'] == None:
        return redirect("/auth")
    context = {'authenticated' : True, 'user' : request.session['user']}

    username = request.session['user']['username']

    database = DatabaseConnection()
    select_query = f"SELECT * FROM TAYANGAN_TERUNDUH TT WHERE TT.username = '{username}' AND TT.id_tayangan = '{id_tayangan}'"
    daftar_unduhan = database.query(select_query)

    if not daftar_unduhan:
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        insert_query = f"INSERT INTO TAYANGAN_TERUNDUH VALUES('{id_tayangan}','{username}','{timestamp}');"
        database.query(insert_query)
    
    return redirect('/fakhri-hijau/tayangan')