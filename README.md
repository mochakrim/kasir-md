# 💻 Dokumentasi Arsitektur & Pembuatan: kasir-md

Dokumen ini berisi catatan teknis, prinsip desain arsitektur, alur logika kode, serta panduan pengembangan sistem **kasir-md** yang dibangun menggunakan **Python murni** (*zero-dependency*) dan **Markdown** sebagai brankas data (*Database-as-Text*).

---

## 🎯 Filosofi & Prinsip Desain Sistem

1. **Zero-Dependency & Super Ringan:**
   Tidak menggunakan *database* berat (SQL/NoSQL) maupun *framework* antarmuka eksternal yang membebani RAM. Sistem murni mengandalkan pustaka bawaan Python 3 (`http.server`, `json`, `glob`, `os`, `datetime`) dan antarmuka HTML/CSS/JS standar agar berjalan instan di perangkat spesifikasi rendah.
2. **Database-as-Markdown (`.md`):**
   Seluruh penyimpanan data (katalog harga, arsip struk, hingga rekap harian) menggunakan format teks polos Markdown. Keunggulannya adalah ukuran file sangat kecil (hitungan byte/KB), bebas *corrupt*, dapat dibuka di editor teks mana pun, dan mudah dilacak riwayat perubahannya.
3. **Time-Based Sharding (Pemisahan per Tanggal):**
   Data barang tidak ditumpuk dalam satu file raksasa. Setiap pembaruan harga disimpan dalam file baru berurut tanggal (`harga_YYYY_MM_DD.md`). Saat dimuat, Python membaca file secara berurutan dari tanggal terlama hingga terbaru sehingga harga baru otomatis menimpa (*override*) harga lama berdasarkan `Kode` barang.

---

## 🏗️ Arsitektur & Alur Kerja Program

Sistem bekerja dengan memisahkan lapisan logika (*backend*) dan lapisan tampilan (*frontend*) agar kode mudah dirawat dan bebas *error*:

```text
[ File Harga .md ] ──(Dibaca urut tanggal)──> [ kasir_web.py (Server Lokal) ]
                                                        │  ▲
                                    (JSON Data Produk)  │  │ (POST Transaksi / GET Rekap)
                                                        ▼  │
                                              [ index.html (Browser UI) ]
                                                        │
                                                        ▼
                                     [ Arsip Struk .md & Laporan Rekap .md ]
```

### Rincian Peran Setiap File
* **`kasir_web.py` (Backend & Data Engine):**
  * `muat_database_md()`: Memindai folder `data/*.md`, mem-parsing baris tabel Markdown berdasarkan pemisah pipa (`|`), membersihkan format angka, dan menyusun kamus produk terkini.
  * `simpan_struk_md()`: Menerima daftar belanjaan beserta nominal tunai, menghitung kembalian, memformat teks presisi lebar 32 karakter (kertas thermal 58mm), dan menyimpannya ke `struk/struk_YYYYMMDD_HHMMSS.md`.
  * `buat_rekap_harian_md()`: Memindai seluruh file struk pada tanggal hari ini, menjumlahkan baris `TOTAL`, dan menghasilkan laporan tabel Markdown di `laporan/rekap_YYYYMMDD.md`.
  * `KasirHandler`: Menangani permintaan HTTP lokal pada *port* `8080` (`GET /`, `GET /api/produk`, `GET /api/rekap`, dan `POST /api/bayar`).
* **`index.html` (Frontend / Antarmuka Kasir):**
  * Menangani pencarian barang *real-time* di sisi klien (memori browser) agar filter barang berjalan instan tanpa membebani server.
  * Mengelola keranjang belanja sementara, penghapusan item salah pencet (`splice` array), kalkulator kembalian tunai, dan validasi pembayaran.
* **`BukaKasir.sh` (Skrip Otomasi Shell):**
  * Skrip Bash khusus lingkungan Termux Android untuk berpindah direktori ke `kasir-md`, menjalankan `kasir_web.py` di latar belakang (`&`), dan memicu *intent* pembukaan browser otomatis ke `http://localhost:8080`.

---

## 🛠️ Panduan Pengembangan & Modifikasi (Untuk Pembuat)

### 1. Lingkungan Uji Coba (iOS / iPadOS via a-Shell)
1. Buka terminal **a-Shell** dan arahkan ke direktori proyek:
   ```bash
   cd kasir-md
   ```
2. Jalankan server dalam mode pengembangan untuk memantau log HTTP (`200` / `500`) dan pesan *error* secara langsung:
   ```bash
   python kasir_web.py
   ```
3. Buka **`http://localhost:8080`** di Safari. Setiap kali mengubah kode di `index.html`, cukup *refresh* browser. Jika mengubah kode di `kasir_web.py`, hentikan server (`Ctrl + C`) lalu jalankan ulang.

### 2. Titik Kustomisasi Kode
* **Mengubah Nama & Alamat Toko di Struk:** Edit daftar teks header di dalam fungsi `simpan_struk_md()` pada file `kasir_web.py`.
* **Mengubah Port Server:** Ubah angka `8080` pada baris paling bawah `kasir_web.py` (`HTTPServer(("0.0.0.0", 8080), ...)`) serta pada skrip `BukaKasir.sh` jika *port* bentrok dengan layanan lain.
* **Menambah Fitur Baru (Pengembangan Lanjutan):**
  * *Manajemen Stok Otomatis:* Menambahkan kolom `Stok` pada tabel `.md` dan membuat fungsi pengurang stok setiap transaksi berhasil.
  * *Export ke CSV/Excel:* Menambahkan modul bawaan `csv` di Python untuk mengonversi folder `laporan/` menjadi file spreadsheet bulanan.
