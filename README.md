# Proyek Django - Daftar Transaksi

Proyek ini adalah aplikasi Django sederhana yang memungkinkan pengguna untuk melihat dan memfilter data transaksi berdasarkan **Nama Klien** dan **Tanggal**. Aplikasi ini menggunakan **SQLite** sebagai database untuk menyimpan dan menampilkan data.

## Struktur Proyek

```
daoa/
├── manage.py
├── daoa/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── app/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── templates/
    │   └── app/
    │       └── transaksi.html
    └── migrations/
        └── __init__.py
```

## Deskripsi Fitur

* **Daftar Transaksi**: Aplikasi ini menampilkan daftar transaksi yang berisi **Nama Klien** dan **Tanggal**.
* **Filter Data**: Pengguna dapat memfilter data transaksi berdasarkan **Nama Klien** dan **Tanggal** melalui dropdown yang tersedia.
* **SQLite Database**: Database digunakan untuk menyimpan data transaksi.

## Langkah-langkah untuk Menjalankan Proyek

1. **Clone atau Unduh Proyek**:
   Pertama, clone atau unduh proyek ini ke dalam komputer kamu.

2. **Install Dependensi**:
   Pastikan kamu memiliki Python dan Django terinstal di sistem kamu. Jika belum, instal Django menggunakan pip:

   ```bash
   pip install django
   ```

3. **Jalankan Migrasi**:
   Meskipun proyek ini menggunakan file database SQLite, kamu tetap perlu menjalankan migrasi untuk membuat struktur database yang diperlukan:

   ```bash
   python manage.py migrate
   ```

4. **Menjalankan Server Django**:
   Setelah migrasi selesai, jalankan server Django dengan perintah berikut:

   ```bash
   python manage.py runserver
   ```

   Akses aplikasi di browser dengan membuka:
   `http://127.0.0.1:8000/`

5. **Akses Admin Panel**:
   Untuk menambahkan data transaksi melalui Admin Panel, buat superuser menggunakan perintah:

   ```bash
   python manage.py createsuperuser
   ```

   Setelah itu, akses Admin Panel di:
   `http://127.0.0.1:8000/admin/`

## Penjelasan Kode

### **Model** (`app/models.py`)

Aplikasi ini tidak menggunakan model secara langsung di dalam database karena data transaksi sudah disediakan melalui file JSON (`data.json`). Namun, jika kamu ingin mengonversi data menjadi model yang lebih dinamis, kamu bisa menambahkan model di sini untuk menyimpan data di database.

```python
class Transaksi(models.Model):
    nama_klien = models.CharField(max_length=255)
    tanggal = models.DateField()
    
    def __str__(self):
        return f"{self.nama_klien} - {self.tanggal}"
```

### **View** (`app/views.py`)

Pada bagian ini, kita membuat view `transaksi_view` untuk menampilkan data transaksi, dan juga untuk menangani proses filter berdasarkan **Nama Klien** dan **Tanggal**.

```python
from django.shortcuts import render
import json
import os
from django.conf import settings

def transaksi_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'app', 'data.json')
    with open(file_path) as f:
        data = json.load(f)

    selected_klien = request.GET.get('nama_klien')
    selected_tanggal = request.GET.get('tanggal')

    # Filter berdasarkan Nama Klien
    data_filtered = [d for d in data if not selected_klien or d['nama_klien'] == selected_klien]

    # Menyusun daftar Nama Klien dan Tanggal
    semua_klien = sorted(set(d['nama_klien'] for d in data))
    tanggal_tersedia = sorted(set(d['tanggal'] for d in data_filtered))

    # Filter berdasarkan Tanggal
    if selected_tanggal:
        data_filtered = [d for d in data_filtered if d['tanggal'] == selected_tanggal]

    # Kirim data ke template
    context = {
        'data': data_filtered,
        'semua_klien': semua_klien,
        'tanggal_tersedia': tanggal_tersedia,
        'selected_klien': selected_klien,
        'selected_tanggal': selected_tanggal,
    }
    return render(request, 'app/transaksi.html', context)
```

Di sini, kita membaca file `data.json`, memfilter data berdasarkan parameter `nama_klien` dan `tanggal` yang dikirimkan melalui query string (`GET`), dan mengirim data yang sudah difilter ke template `transaksi.html`.

### **Template** (`app/templates/app/transaksi.html`)

File template ini digunakan untuk menampilkan data dalam bentuk tabel dan menyediakan dropdown untuk filter data.

```html
<h2>Daftar Transaksi</h2>

<table border="1" cellpadding="5" cellspacing="0">
  <tr>
    <th>Nama Klien</th>
    <th>Tanggal</th>
  </tr>
  {% for row in data %}
    <tr>
      <td>{{ row.nama_klien }}</td>
      <td>{{ row.tanggal }}</td>
    </tr>
  {% empty %}
    <tr><td colspan="2">Tidak ada data</td></tr>
  {% endfor %}
</table>

<h3>Filter Data</h3>
<form method="get">
  <label>Nama Klien:</label>
  <select name="nama_klien" onchange="this.form.submit()">
    <option value="">-- Semua Klien --</option>
    {% for klien in semua_klien %}
      <option value="{{ klien }}" {% if klien == selected_klien %}selected{% endif %}>{{ klien }}</option>
    {% endfor %}
  </select>

  <label>Tanggal:</label>
  <select name="tanggal" onchange="this.form.submit()">
    <option value="">-- Semua Tanggal --</option>
    {% for tgl in tanggal_tersedia %}
      <option value="{{ tgl }}" {% if tgl == selected_tanggal %}selected{% endif %}>{{ tgl }}</option>
    {% endfor %}
  </select>
</form>
```

Template ini menampilkan tabel dengan data transaksi dan menyediakan dua dropdown untuk **Nama Klien** dan **Tanggal**. Data dalam tabel akan otomatis diperbarui setiap kali pengguna memilih opsi dari dropdown.

---

## Penjelasan Proses Filtering

1. **Nama Klien**: Data transaksi dapat difilter berdasarkan **Nama Klien** yang dipilih di dropdown.
2. **Tanggal**: Setelah memfilter berdasarkan **Nama Klien**, kamu juga bisa memfilter data berdasarkan **Tanggal** transaksi.

---

### 14. **URL Routing**

URL routing ditangani dalam file `urls.py`:

```python
# app/urls.py
from django.urls import path
from .views import transaksi_view

urlpatterns = [
    path('', transaksi_view, name='transaksi'),
]
```

Di file `daoa/urls.py`, kita meng-include URL dari aplikasi `app`:

```python
# daoa/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
```

---

## Kesimpulan

* **Data**: Aplikasi ini menggunakan **data JSON** sebagai sumber data untuk transaksi.
* **Filter**: Pengguna dapat memfilter transaksi berdasarkan **Nama Klien** dan **Tanggal**.
* **Admin Panel**: Menyediakan panel admin untuk menambahkan dan mengelola transaksi.

Jika ada pertanyaan lebih lanjut atau butuh bantuan lebih lanjut, jangan ragu untuk menghubungi kami!
