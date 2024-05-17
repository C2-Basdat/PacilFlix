from django.shortcuts import render, redirect
from utils import DatabaseConnection
from datetime import datetime, timedelta, date
import psycopg2


# Create your views here.
QUERY_TAYANGAN_TERBAIK = """
WITH episode_durations AS (
    SELECT 
        e.id_series AS id_tayangan,
        SUM(e.durasi) AS total_duration
    FROM 
        EPISODE e
    GROUP BY 
        e.id_series
),
watched_duration AS (
    SELECT 
        rn.id_tayangan, 
        rn.username, 
        rn.start_date_time, 
        rn.end_date_time,
        EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60 AS watched_minutes, -- Convert to minutes
        COALESCE(f.durasi_film, ed.total_duration) AS total_duration
    FROM 
        RIWAYAT_NONTON rn
    LEFT JOIN 
        FILM f ON rn.id_tayangan = f.id_tayangan
    LEFT JOIN 
        episode_durations ed ON rn.id_tayangan = ed.id_tayangan
    WHERE 
        rn.start_date_time >= NOW() - INTERVAL '7 days'
),
views_count AS (
    SELECT 
        t.id AS id_tayangan, 
        COUNT(wd.id_tayangan) AS view_count
    FROM 
        TAYANGAN t
    LEFT JOIN 
        watched_duration wd ON t.id = wd.id_tayangan AND wd.watched_minutes >= wd.total_duration * 0.7
    GROUP BY 
        t.id
),
ranked_shows AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY vc.view_count DESC) AS peringkat,
        t.id,
        t.judul,
        t.sinopsis,
        t.url_video_trailer AS url_trailer,
        t.release_date_trailer AS tanggal_rilis_trailer,
        vc.view_count AS tayangan_terbaik
    FROM 
        views_count vc
    JOIN 
        TAYANGAN t ON vc.id_tayangan = t.id
)
SELECT 
    rs.peringkat,
    rs.id,
    rs.judul,
    rs.sinopsis as sinopsis_trailer,
    rs.url_trailer as url_video_trailer,
    rs.tanggal_rilis_trailer as release_date_trailer,
    rs.tayangan_terbaik as total_view_7_hari_terakhir
FROM 
    ranked_shows rs
ORDER BY 
    rs.peringkat
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

    if 'user' in request.session:
        context['authenticated'] = True
        context['username'] = request.session['user']['username']
    else:
        context['authenticated'] = False
    
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
            hasil_cari_tayangan = database.query(f"SELECT id, judul, sinopsis_trailer, url_video_trailer, release_date_trailer FROM TAYANGAN WHERE judul ilike '%{judul}%';")
            context['hasil_cari_tayangan'] = hasil_cari_tayangan
    
    if 'user' in request.session:
        context['authenticated'] = True
        context['username'] = request.session['user']['username']
    else:
        context['authenticated'] = False
        return redirect("authentication:show_auth")
    
    context['have_paket'] = database.query(f"SELECT EXISTS (SELECT 1 FROM transaction WHERE username = '{context['username']}' AND end_date_time > CURRENT_DATE AND timestamp_pembayaran = (SELECT MAX(timestamp_pembayaran) FROM transaction WHERE username = '{context['username']}')) AS user_exists;")[0]['user_exists']
        
    return render(request, 'tayangan.html', context)

def read_film_series(request, id_tayangan):
    context = {}
    database = DatabaseConnection()

    if 'user' not in request.session:
        context['authenticated'] = False
        return redirect("authentication:show_auth")
    
    context['authenticated'] = True
    context['username'] = request.session['user']['username']
    
    is_film = list(database.query(f"select * from film where id_tayangan='{str(id_tayangan)}';"))
    if len(is_film):
        context['is_film'] = True

        if request.method == "POST":
            durasi_nonton = request.POST.get("durasi")
            raw = database.query(f"select durasi_film as durasi from film where id_tayangan = '{id_tayangan}';")
            durasi_film = int(raw[0]['durasi'])
            durasi_minutes = (float(durasi_nonton) / 100) * durasi_film 

            now = datetime.now()
            end = now + timedelta(minutes=durasi_minutes)

            formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
            formatted_end = end.strftime("%Y-%m-%d %H:%M:%S")

            insert = database.query(f"INSERT INTO RIWAYAT_NONTON VALUES('{id_tayangan}','{context['username']}','{formatted_now}','{formatted_end}');")
            print(insert)
        
        data_film = query_data_film(database, id_tayangan)
        context['data_film'] = data_film
    else:
        context['is_film'] = False
        data_series = query_data_series(database, id_tayangan)
        context['data_series'] = data_series
    return render(request, 'film_series.html', context)


def download_tayangan(request, id_tayangan):
    database = DatabaseConnection()

    if 'user' not in request.session:
        return redirect("authentication:show_auth")
    username = request.session['user']['username']

    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    
    database.query(f"INSERT INTO TAYANGAN_TERUNDUH VALUES('{id_tayangan}','{username}','{formatted_now}');")
    return redirect('read_tayangan')

def read_episode(request):
    database = DatabaseConnection()
    context = {}

    if 'user' not in request.session:
        context['authenticated'] = False
        return redirect("authentication:show_auth")
    
    context['authenticated'] = True
    context['username'] = request.session['user']['username']

    if request.method == "GET":
        id_tayangan = request.GET.get('id_tayangan')
        judul_episode = request.GET.get('judul_episode')
        context['data'] = query_data_episode(database, id_tayangan, judul_episode)

    if request.method == "POST":
        id_tayangan = request.POST.get('id_tayangan')
        judul_episode = request.POST.get('judul_episode')
        durasi_nonton = request.POST.get('durasi')
        raw = database.query(f"select durasi from episode where id_series = '{id_tayangan}' and sub_judul = '{judul_episode}';")

        durasi_episode = int(raw[0]['durasi'])
        durasi_minutes = (float(durasi_nonton) / 100) * durasi_episode 

        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

        end = now + timedelta(minutes=durasi_minutes)
        formatted_end = end.strftime("%Y-%m-%d %H:%M:%S")

        insert = database.query(f"INSERT INTO RIWAYAT_NONTON VALUES('{id_tayangan}','{context['username']}','{formatted_now}','{formatted_end}');")
        print(insert)
        context['data'] = query_data_episode(database, id_tayangan, judul_episode)

    return render(request, 'episode.html', context)

def create_read_ulasan(request):
    database = DatabaseConnection()
    context = {'already_reviewed':False}

    if 'user' not in request.session:
        context['authenticated'] = False
        return redirect("authentication:show_auth")
    
    context['authenticated'] = True
    context['username'] = request.session['user']['username']

    if request.method == "GET":
        id_tayangan = request.GET.get('id_tayangan')
        context['data_id_tayangan'] = id_tayangan
        context['reviews'] = database.query(f"SELECT * FROM ULASAN WHERE id_tayangan = '{id_tayangan}' order by timestamp DESC;")
        context['titles'] = database.query(f"select judul from tayangan where id = '{id_tayangan}';")

    if request.method == "POST":
        id_tayangan = request.POST.get('id_tayangan')
        deskripsi = request.POST.get('deskripsi')
        rating = request.POST.get('rating')

        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        insert_response = database.query(f"INSERT INTO ULASAN VALUES('{id_tayangan}','{context['username']}','{formatted_now}',{int(rating)},'{deskripsi}');")
        if isinstance(insert_response, psycopg2.errors.RaiseException):
            context['already_reviewed'] = True
        

        context['data_id_tayangan'] = id_tayangan
        context['reviews'] = database.query(f"SELECT * FROM ULASAN WHERE id_tayangan = '{id_tayangan}' order by timestamp DESC;")
        context['titles'] = database.query(f"select judul from tayangan where id = '{id_tayangan}';")

    return render(request, 'ulasan.html', context)


def query_data_episode(database, id_tayangan, judul_episode):
    query_episode = f"SELECT t.id,t.judul AS judul,e.sub_judul AS subjudul,e.sinopsis AS sinopsis_episode,e.durasi AS durasi_episode,e.url_video AS url_episode,(SELECT STRING_AGG(sub_judul, ', ') FROM EPISODE WHERE id_series = '{id_tayangan}' AND sub_judul != '{judul_episode}') AS episode_lainnya,e.release_date AS tanggal_rilis_episode FROM TAYANGAN t JOIN EPISODE e ON t.id = e.id_series GROUP BY t.id, t.judul, e.sub_judul, e.sinopsis, e.durasi, e.url_video, e.release_date having t.id = '{id_tayangan}' and e.sub_judul = '{judul_episode}';"
    hasil = database.query(query_episode)
    for i in range(len(hasil)):
        hasil[i]['episode_lainnya'] = str(hasil[i]['episode_lainnya']).split(", ")

        # Cek dah rilis atau belom -> asumsinya kita bisa langsung nonton meskipun baru rilis di hari tersebut
        current_date = datetime.now().date()
        if current_date < hasil[i]['tanggal_rilis_episode']:
            hasil[i]['released'] = False
        else:
            hasil[i]['released'] = True
    return hasil

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
    query_film += f"HAVING t.id = '{id_tayangan}';"
    data_film = database.query(query_film)
    for i in range(len(data_film)):
        data_film[i]['average_rating'] = float(data_film[i]['average_rating'])
        data_film[i]['actors'] = str(data_film[i]['actors']).split(", ")
        data_film[i]['writers'] = str(data_film[i]['writers']).split(", ")
        data_film[i]['genres'] = str(data_film[i]['genres']).split(", ")

        # Cek dah rilis atau belom
        current_date = datetime.now().date()
        if current_date < data_film[i]['release_date']:
            data_film[i]['released'] = False
        else:
            data_film[i]['released'] = True
    return data_film

def query_data_series(database, id_tayangan):
    query_series = """
                 WITH episode_durations AS (
                    SELECT 
                        e.id_series,
                        SUM(e.durasi) AS total_duration
                    FROM 
                        EPISODE e
                    GROUP BY 
                        e.id_series
                ),
                total_views AS (
                    SELECT 
                        rn.id_tayangan,
                        COUNT(*) AS total_views
                    FROM 
                        RIWAYAT_NONTON rn
                    JOIN 
                        episode_durations ed ON rn.id_tayangan = ed.id_series
                    WHERE 
                        EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60 >= ed.total_duration * 0.7
                    GROUP BY 
                        rn.id_tayangan
                )
                SELECT 
                    t.id AS series_id,
                    t.judul AS title,
                    t.sinopsis AS synopsis,
                    ed.total_duration AS total_duration,
                    STRING_AGG(DISTINCT e.url_video, ', ') AS url_episodes,
                    STRING_AGG(DISTINCT e.sub_judul, ', ') AS judul_episodes,
                    MIN(e.release_date) AS release_date,
                    AVG(u.rating) AS average_rating,
                    STRING_AGG(DISTINCT gt.genre, ', ') AS genres,
                    t.asal_negara AS country,
                    STRING_AGG(DISTINCT c_actors.nama, ', ') AS actors,
                    STRING_AGG(DISTINCT c_writers.nama, ', ') AS writers,
                    c_directors.nama AS director,
                    COALESCE(tv.total_views, 0) AS total_views
                FROM 
                    TAYANGAN t
                JOIN
                    SERIES s ON t.id = s.id_tayangan
                JOIN 
                    episode_durations ed ON t.id = ed.id_series
                LEFT JOIN 
                    EPISODE e ON t.id = e.id_series
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
                    SUTRADARA st ON t.id_sutradara = st.id
                LEFT JOIN 
                    CONTRIBUTORS c_directors ON st.id = c_directors.id
                LEFT JOIN 
                    total_views tv ON t.id = tv.id_tayangan
                GROUP BY 
                    t.id, t.judul, t.sinopsis, ed.total_duration, t.asal_negara, c_directors.nama, tv.total_views
                    """
    query_series += f"HAVING t.id = '{id_tayangan}';"
    data_series = database.query(query_series)
    for i in range(len(data_series)):
        data_series[i]['average_rating'] = float(data_series[i]['average_rating'])
        data_series[i]['url_episodes'] = str(data_series[i]['url_episodes']).split(", ")
        data_series[i]['judul_episodes'] = str(data_series[i]['judul_episodes']).split(", ")
        data_series[i]['judul_url_episodes'] = zip(data_series[i]['judul_episodes'], data_series[i]['url_episodes'])
        data_series[i]['actors'] = str(data_series[i]['actors']).split(", ")
        data_series[i]['writers'] = str(data_series[i]['writers']).split(", ")
        data_series[i]['genres'] = str(data_series[i]['genres']).split(", ")
    return data_series

