## Penjelasan Fitur Filter

Aplikasi ini menyediakan dua opsi filter yang memungkinkan pengguna untuk menyaring data transaksi berdasarkan **Nama Klien** dan **Tanggal**. Penjelasan tentang cara kerja filter adalah sebagai berikut:

### 1. **Filter Berdasarkan Nama Klien**

Pada bagian ini, pengguna dapat memilih nama klien dari dropdown yang tersedia. Jika tidak ada nama klien yang dipilih (opsi default **"-- Semua Klien --"**), maka semua transaksi akan ditampilkan. Jika pengguna memilih nama klien tertentu, maka hanya transaksi yang memiliki nama klien tersebut yang akan ditampilkan.

* **Dropdown** akan menampilkan daftar semua nama klien yang ada pada data transaksi.
* **Data yang ditampilkan** akan difilter berdasarkan nilai **`nama_klien`** yang dipilih.

Di dalam **view** (`transaksi_view`), proses ini dilakukan dengan kode berikut:

```python
selected_klien = request.GET.get('nama_klien')
data_filtered = [d for d in data if not selected_klien or d['nama_klien'] == selected_klien]
```

Jika **`selected_klien`** dipilih, data yang ditampilkan hanya yang sesuai dengan klien tersebut.

### 2. **Filter Berdasarkan Tanggal**

Setelah memilih **Nama Klien**, pengguna dapat memilih **Tanggal** dari dropdown yang kedua. Dropdown ini akan menampilkan tanggal yang tersedia dalam data yang sudah difilter berdasarkan nama klien. Jika tidak ada tanggal yang dipilih (opsi default **"-- Semua Tanggal --"**), maka semua tanggal transaksi untuk klien yang dipilih akan ditampilkan.

Proses filtering tanggal dilakukan dengan kode berikut:

```python
tanggal_tersedia = sorted(set(d['tanggal'] for d in data_filtered))
if selected_tanggal:
    data_filtered = [d for d in data_filtered if d['tanggal'] == selected_tanggal]
```

Jika **`selected_tanggal`** dipilih, data akan difilter lagi hanya menampilkan transaksi dengan tanggal yang dipilih.

### 3. **Logika Filter secara Bersamaan**

Kedua filter (Nama Klien dan Tanggal) bisa digunakan bersamaan. Jika pengguna memilih **Nama Klien** dan kemudian memilih **Tanggal**, maka data transaksi yang ditampilkan akan disaring terlebih dahulu berdasarkan Nama Klien, kemudian lebih lanjut difilter berdasarkan Tanggal yang dipilih.

### 4. **Formulir Filter**

Formulir filter menggunakan method `GET`, yang berarti nilai yang dipilih oleh pengguna akan ditambahkan sebagai query string pada URL. Setiap kali pengguna memilih nilai baru pada dropdown filter (baik untuk Nama Klien maupun Tanggal), formulir akan disubmit otomatis, yang menyebabkan halaman dimuat ulang dengan data yang sudah difilter sesuai dengan pilihan pengguna.

```html
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

Formulir ini memungkinkan pengguna untuk memilih filter, dan setiap kali pilihan berubah, data akan langsung difilter berdasarkan pilihan tersebut tanpa perlu memuat halaman secara manual.
