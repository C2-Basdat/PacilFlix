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