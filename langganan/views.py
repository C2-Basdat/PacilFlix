from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from utils import DatabaseConnection

def index(request):
    if 'user' not in request.session:
        return redirect("authentication:show_auth")

    database = DatabaseConnection()
    username = request.session['user']['username']
    query_active = f"""
    WITH dukungan_perangkat_agg AS (
        SELECT
            p.nama,
            STRING_AGG(dp.dukungan_perangkat, ', ') AS dukungan_perangkat
        FROM
            paket p
            LEFT JOIN dukungan_perangkat dp ON p.nama=dp.nama_paket
        GROUP BY
            p.nama
    )
    SELECT
        p.nama,
        p.harga,
        p.resolusi_layar,
        dp.dukungan_perangkat,
        t.start_date_time,
        t.end_date_time
    FROM
        pengguna u
        JOIN transaction t on u.username=t.username
        JOIN paket p on p.nama=t.nama_paket
        JOIN dukungan_perangkat_agg dp on p.nama=dp.nama
    WHERE
        u.username='{username}'
        AND CURRENT_DATE BETWEEN t.start_date_time AND t.end_date_time
    ORDER BY
        t.timestamp_pembayaran DESC
    LIMIT 1;
    """
    
    query_package = """
    WITH dukungan_perangkat_agg AS (
        SELECT
            p.nama,
            STRING_AGG(dp.dukungan_perangkat, ', ') AS dukungan_perangkat
        FROM
            paket p
            LEFT JOIN dukungan_perangkat dp ON p.nama=dp.nama_paket
        GROUP BY
            p.nama
    )
    SELECT
        p.nama,
        p.harga,
        p.resolusi_layar,
        dp.dukungan_perangkat
    FROM
        paket p
        JOIN dukungan_perangkat_agg dp on p.nama=dp.nama
    ORDER BY
        p.harga ASC;
    """

    query_transactions = f"""
    SELECT
        p.nama,
        t.start_date_time,
        t.end_date_time,
        t.metode_pembayaran,
        t.timestamp_pembayaran,
        p.harga
    FROM
        transaction t
        JOIN paket p ON t.nama_paket=p.nama
        JOIN pengguna u ON t.username=u.username
    WHERE
        u.username='{username}'
    ORDER BY
        t.timestamp_pembayaran DESC;
    """

    active_package = database.query(query_active)
    all_packages = database.query(query_package)
    all_transactions = database.query(query_transactions)

    context = {
        'active': active_package[0] if active_package else None,
        'packages': all_packages,
        'transactions': all_transactions,
        'authenticated': True,
        'username': request.session['user']['username']
    }

    return render(request, 'langganan.html', context)

def beli(request):
    if 'user' not in request.session:
        return redirect("authentication:show_auth")

    database = DatabaseConnection()
    if request.method == 'GET':
        paket = request.GET.get('paket', None)
        if paket == None:
            return HttpResponseServerError("Error During Error Processing")
        
        query_str = f"""
        WITH dukungan_perangkat_agg AS (
            SELECT
                p.nama,
                STRING_AGG(dp.dukungan_perangkat, ', ') AS dukungan_perangkat
            FROM
                paket p
                LEFT JOIN dukungan_perangkat dp ON p.nama=dp.nama_paket
            GROUP BY
                p.nama
        )
        SELECT
            p.nama,
            p.harga,
            p.resolusi_layar,
            dp.dukungan_perangkat
        FROM
            paket p
            JOIN dukungan_perangkat_agg dp on p.nama=dp.nama
        WHERE
            p.nama ILIKE '{paket}';
        """

        package = database.query(query_str)

        context = {
            'paket': package[0],
            'authenticated': True,
            'username': request.session['user']['username']
        }

        return render(request, 'beli.html', context)
    elif request.method == 'POST':
        if 'user' not in request.session:
            return redirect("/auth")
        username = request.session['user']['username']
        paket = request.POST.get('paket')
        payment_method = request.POST.get('method')

        query_str = f"""
        INSERT INTO
            transaction
        VALUES
            ('{username}', CURRENT_DATE, CURRENT_DATE + INTERVAL '1' MONTH, '{paket}', '{payment_method}', NOW()::timestamp(0));
        """

        result = database.query(query_str)

        return redirect('langganan:index')