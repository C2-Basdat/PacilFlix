from datetime import datetime
from django.shortcuts import redirect, render

from utils import DatabaseConnection

def show_daftar_favorit(request):
    # verify login
    if 'user' not in request.session:
        return redirect("/auth")
    context = {'authenticated' : True, 'user' : request.session['user']}

    username = request.session['user']['username']
    query = f"SELECT * FROM DAFTAR_FAVORIT DF WHERE DF.username = '{username}'"
    
    database = DatabaseConnection()
    daftar_favorit = database.query(query)

    context['daftar_favorit'] = daftar_favorit
    
    return render(request, 'daftar_favorit.html', context)

def add_daftar_favorit(request, judul):
    # verify login
    if 'user' not in request.session:
        return redirect("/auth")
    context = {'authenticated' : True, 'user' : request.session['user']}

    username = request.session['user']['username']
    select_query = f"SELECT * FROM DAFTAR_FAVORIT DF WHERE DF.username = '{username}' AND DF.judul = '{judul}'"

    database = DatabaseConnection()
    daftar_favorit = database.query(select_query)

    if not daftar_favorit:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_query = f"INSERT INTO DAFTAR_FAVORIT (timestamp, username, judul) VALUES('{timestamp}', '{username}', '{judul}')"

        database.query(insert_query)

    return redirect("/fakhri-hijau/tayangan")

def delete_daftar_favorit(request, judul):
    # verify login
    if 'user' not in request.session:
        return redirect("/auth")
    context = {'authenticated' : True, 'user' : request.session['user']}

    username = request.session['user']['username']
    delete_query = f"DELETE FROM DAFTAR_FAVORIT DF WHERE DF.username = '{username}' AND DF.judul = '{judul}'"

    database = DatabaseConnection()
    database.query(delete_query)

    return redirect("/daftar-favorit")