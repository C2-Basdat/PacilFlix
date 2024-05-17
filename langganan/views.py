from django.shortcuts import render
from utils import DatabaseConnection

def index(request):
    database = DatabaseConnection()
    username = 'bob'
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
        u.username='alice'
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
        'transactions': all_transactions
    }

    return render(request, 'langganan.html', context)

def beli(request):
    return render(request, 'beli.html', {})