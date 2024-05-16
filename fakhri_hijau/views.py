from django.shortcuts import render
from utils import DatabaseConnection

# Create your views here.

QUERY_TAYANGAN_TERBAIK = """
SELECT
    ROW_NUMBER() OVER (ORDER BY COALESCE(view_count.Total_View_7_Hari_Terakhir, 0) DESC) AS peringkat,
    t.id as id,
    t.judul AS judul,
    t.sinopsis AS sinopsis,
    t.sinopsis_trailer AS sinopsis_trailer,
    t.url_video_trailer AS url_video_trailer,
    t.release_date_trailer AS release_date_trailer,
    COALESCE(view_count.Total_View_7_Hari_Terakhir, 0) AS total_view_7_hari_terakhir
FROM
    TAYANGAN t
LEFT JOIN (
    SELECT
        id_tayangan,
        COUNT(*) AS Total_View_7_Hari_Terakhir
    FROM
        RIWAYAT_NONTON
    WHERE
        start_date_time BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
    GROUP BY
        id_tayangan
) view_count ON t.id = view_count.id_tayangan
ORDER BY
    Total_View_7_Hari_Terakhir DESC
LIMIT 10;
"""

def read_trailer(request):
    database = DatabaseConnection()
    query_trailer_film = f"SELECT A.judul, A.sinopsis_trailer, A.url_video_trailer, A.release_date_trailer FROM TAYANGAN A, FILM B WHERE A.id = B.id_tayangan;"
    query_trailer_series = f"SELECT A.judul, A.sinopsis_trailer, A.url_video_trailer, A.release_date_trailer FROM TAYANGAN A, SERIES B WHERE A.id = B.id_tayangan;"
    
    tayangan_terbaik = database.query(QUERY_TAYANGAN_TERBAIK)
    trailer_film = database.query(query_trailer_film)
    trailer_series = database.query(query_trailer_series)
    context = {'tayangan_terbaik': tayangan_terbaik, 'trailer_film': trailer_film, 'trailer_series': trailer_series}
    
    if request.method == "GET":
        judul = request.GET.get('judul', '')
        if judul:
            # Lakukan pencarian berdasarkan judul film
            hasil_cari_tayangan = database.query(f"SELECT id, judul, sinopsis_trailer, url_video_trailer, release_date_trailer FROM TAYANGAN WHERE judul ilike '%{judul}%'")
            context['hasil_cari_tayangan'] = hasil_cari_tayangan
        
    return render(request, 'trailer.html', context)

def read_tayangan(request):
    database = DatabaseConnection()
    query_tayangan_film = f"SELECT A.id, A.judul, A.sinopsis_trailer, A.url_video_trailer, A.release_date_trailer FROM TAYANGAN A, FILM B WHERE A.id = B.id_tayangan;"
    query_tayangan_series = f"SELECT A.id, A.judul, A.sinopsis_trailer, A.url_video_trailer, A.release_date_trailer FROM TAYANGAN A, SERIES B WHERE A.id = B.id_tayangan;"
    
    tayangan_terbaik = database.query(QUERY_TAYANGAN_TERBAIK)
    tayangan_film = database.query(query_tayangan_film)
    tayangan_series = database.query(query_tayangan_series)
    context = {'tayangan_terbaik': tayangan_terbaik, 'tayangan_film': tayangan_film, 'tayangan_series': tayangan_series}
    
    if request.method == "GET":
        judul = request.GET.get('judul', '')
        if judul:
            # Lakukan pencarian berdasarkan judul film
            hasil_cari_tayangan = database.query(f"SELECT id, judul, sinopsis_trailer, url_video_trailer, release_date_trailer FROM TAYANGAN WHERE judul ilike '%{judul}%'")
            context['hasil_cari_tayangan'] = hasil_cari_tayangan
        
    return render(request, 'tayangan.html', context)

def read_film_series(request, id_tayangan):
    context = {}
    database = DatabaseConnection()
    is_film = list(database.query(f"SELECT EXISTS (SELECT 1 FROM film WHERE id_tayangan = '{str(id_tayangan)}')"))[0]
    
    if is_film['exists']:
        context['is_film'] = True
        data_film = query_data_film(database, id_tayangan)
        context['data_film'] = data_film
    else:
        context['is_film'] = False
        # context['info_series']
    
    return render(request, 'film_series.html', context)


def query_data_film(database, id_tayangan):
    query_film = """
                    SELECT 
                        t.id AS film_id,
                        t.judul AS title,
                        t.sinopsis AS synopsis,
                        f.durasi_film AS duration,
                        f.release_date_film AS release_date,
                        f.url_video_film AS url_film,
                        AVG(u.rating) AS average_rating,
                        STRING_AGG(DISTINCT gt.genre, ', ') AS genres,
                        t.asal_negara AS country,
                        STRING_AGG(DISTINCT c_actors.nama, ', ') AS actors,
                        STRING_AGG(DISTINCT c_writers.nama, ', ') AS writers,
                        c_directors.nama AS director,
                        COALESCE(total_views, 0) AS total_views
                    FROM 
                        TAYANGAN t
                    JOIN
                        FILM f ON t.id = f.id_tayangan
                    LEFT JOIN 
                        ULASAN u ON t.id = u.id_tayangan
                    LEFT JOIN 
                        GENRE_TAYANGAN gt ON t.id = gt.id_tayangan
                    LEFT JOIN 
                        memainkan_tayangan mt ON t.id = mt.id_tayangan
                    LEFT JOIN 
                        PEMAIN p ON mt.id_pemain = p.id
                    LEFT JOIN 
                        CONTRIBUTORS c_actors ON p.id = c_actors.id
                    LEFT JOIN
                        menulis_skenario_tayangan mst ON t.id = mst.id_tayangan
                    LEFT JOIN 
                        PENULIS_SKENARIO ps ON mst.id_penulis_skenario = ps.id
                    LEFT JOIN 
                        CONTRIBUTORS c_writers ON ps.id = c_writers.id
                    LEFT JOIN 
                        SUTRADARA s ON t.id_sutradara = s.id
                    LEFT JOIN 
                        CONTRIBUTORS c_directors ON s.id = c_directors.id
                    LEFT JOIN LATERAL
                        (
                            SELECT 
                                id_tayangan,
                                COUNT(*) AS total_views
                            FROM 
                                RIWAYAT_NONTON
                            WHERE 
                                id_tayangan = t.id
                                AND EXTRACT(EPOCH FROM (end_date_time - start_date_time)) / (f.durasi_film * 60) > 0.7
                            GROUP BY 
                                id_tayangan
                        ) rn ON true
                    GROUP BY 
                        t.id, t.judul, t.sinopsis, f.durasi_film, f.release_date_film, f.url_video_film, t.asal_negara, c_directors.nama, total_views
                    """
    query_film += f"HAVING t.id = '{id_tayangan}'"
    data_film = database.query(query_film)
    for i in range(len(data_film)):
        data_film[i]['average_rating'] = float(data_film[i]['average_rating'])
        data_film[i]['actors'] = str(data_film[i]['actors']).split(",")
        data_film[i]['writers'] = str(data_film[i]['writers']).split(",")
        data_film[i]['genres'] = str(data_film[i]['genres']).split(",")
    return data_film

