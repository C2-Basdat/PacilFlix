from django.shortcuts import redirect, render
from utils import DatabaseConnection

def index(request):
    if 'user' not in request.session:
        return redirect("/auth")
    database = DatabaseConnection()

    filter = request.GET.get('filter', None)

    if filter == 'sutradara':
        where_clause = 'WHERE s.id IS NOT NULL'
    elif filter == 'pemain':
        where_clause = 'WHERE p.id IS NOT NULL'
    elif filter == 'skenario':
        where_clause = 'WHERE ps.id IS NOT NULL'
    else:
        where_clause = ''

    query_str = f"""
    SELECT
        nama,
        (CASE
            WHEN type1 IS NULL AND type2 IS NULL AND type3 IS NULL THEN 'Unknown'
            ELSE CONCAT_WS(', ', type1, type2, type3)
        END) as type,
        jenis_kelamin,
        kewarganegaraan
    FROM (
        SELECT
            nama,
            (CASE WHEN s.id IS NOT NULL THEN 'Sutradara' END) AS type1,
            (CASE WHEN p.id IS NOT NULL THEN 'Pemain' END) AS type2,
            (CASE WHEN ps.id IS NOT NULL THEN 'Penulis Skenario' END) AS type3,
            (CASE WHEN c.jenis_kelamin=0 THEN 'Laki-laki' ELSE 'Perempuan' END) as jenis_kelamin,
            kewarganegaraan
        FROM
            CONTRIBUTORS c
            LEFT JOIN SUTRADARA s on c.id=s.id
            LEFT JOIN PEMAIN p on c.id=p.id
            LEFT JOIN PENULIS_SKENARIO ps on c.id=ps.id
            {where_clause}
    );
    """
    contributors = database.query(query_str)
    context = {
        'contributors': contributors
    }
    return render(request, 'kontributor.html', context)