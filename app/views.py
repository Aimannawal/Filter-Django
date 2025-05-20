import json
import os
from django.conf import settings
from django.shortcuts import render

def transaksi_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'app', 'data.json')
    with open(file_path) as f:
        data = json.load(f)

    selected_klien = request.GET.get('nama_klien')
    selected_tanggal = request.GET.get('tanggal')

    data_filtered = [d for d in data if not selected_klien or d['nama_klien'] == selected_klien]

    semua_klien = sorted(set(d['nama_klien'] for d in data))

    tanggal_tersedia = sorted(set(d['tanggal'] for d in data_filtered))

    if selected_tanggal:
        data_filtered = [d for d in data_filtered if d['tanggal'] == selected_tanggal]

    context = {
        'data': data_filtered,
        'semua_klien': semua_klien,
        'tanggal_tersedia': tanggal_tersedia,
        'selected_klien': selected_klien,
        'selected_tanggal': selected_tanggal,
    }
    return render(request, 'app/transaksi.html', context)
