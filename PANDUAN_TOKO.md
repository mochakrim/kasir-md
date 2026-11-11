# 🏪 Panduan Instalasi & Operasional Kasir Toko (`kasir-md`)

Dokumen ini adalah panduan praktis untuk memasang sistem kasir **`kasir-md`** di tablet Android serta standar operasional (SOP) penggunaan harian di meja kasir.

---

## 🛠️ Bagian 1: Cara Pasang di Tablet Android Baru (Cukup Sekali)

1. **Pindahkan Folder Proyek:**
   Salin seluruh folder **`kasir-md`** ke dalam memori internal tablet Android pada bagian folder **`Download`**.
2. **Instal Aplikasi Pendukung:**
   Unduh dan instal dua aplikasi gratis berikut (disarankan melalui toko aplikasi **F-Droid** agar versi terbaru):
   * **Termux** (mesin penjalan sistem).
   * **Termux:Widget** (pembuat tombol pintasan di layar depan).
3. **Siapkan Sistem & Izin Penyimpanan:**
   Buka aplikasi **Termux** di tablet, lalu ketik (atau salin-tempel) perintah di bawah ini satu per satu dan tekan Enter:
   ```bash
   termux-setup-storage
   ```
   *(Klik **Izinkan / Allow** saat muncul permintaan izin akses file).*
   
   Lanjutkan dengan perintah pemasangan otomatis berikut:
   ```bash
   pkg update && pkg install python -y
   mkdir -p ~/.shortcuts
   cp /storage/emulated/0/Download/kasir-md/BukaKasir.sh ~/.shortcuts/
   chmod +x ~/.shortcuts/BukaKasir.sh
   ```
4. **Pasang Tombol Pintasan di Layar Utama Tablet:**
   * Kembali ke layar depan (*Home Screen*) tablet Android.
   * Tekan dan tahan area layar yang kosong $\rightarrow$ pilih menu **Widgets**.
   * Cari **Termux:Widget**, lalu seret ke layar depan.
   * Pilih **`BukaKasir.sh`**. Kini tombol kasir sudah siap digunakan sekali sentuh.

---

## ☀️ Bagian 2: SOP Buka Toko & Melayani Pembeli

1. **Menyalakan Mesin Kasir:**
   Sentuh ikon **`BukaKasir.sh`** di layar depan tablet. Tunggu 1 detik hingga halaman kasir terbuka otomatis di browser Chrome.
2. **Mencatat Belanjaan:**
   * Ketik nama barang di kolom pencarian atas, lalu sentuh tombol barang untuk memasukkannya ke keranjang.
   * **Jika Salah Pencet:** Sentuh tombol merah **`X`** di sebelah kanan nama barang untuk menghapus satu item, atau tekan **Batalkan Semua** untuk mengosongkan keranjang.
3. **Pembayaran & Kembalian:**
   * Masukkan nominal uang yang diberikan pembeli pada kolom **Uang Tunai** (atau gunakan tombol cepat **Uang Pas**, **+10rb**, **+20rb**, **+50rb**, **+100rb**).
   * Perhatikan kotak hijau **Kembalian** untuk memastikan jumlah uang kembalian yang harus diserahkan.
   * Tekan tombol hijau **Bayar & Cetak Struk**. Bukti transaksi otomatis tersimpan di folder `struk/`.
4. **Mencetak Struk ke Printer Bluetooth (Opsional):**
   Buka aplikasi *File Manager* tablet $\rightarrow$ masuk ke folder `Download/kasir-md/struk/` $\rightarrow$ pilih file transaksi terbaru $\rightarrow$ bagikan (*Share*) ke aplikasi printer thermal Bluetooth (seperti **RawBT**).

---

## 🌙 Bagian 3: SOP Tutup Toko & Laporan Omzet

1. Sebelum menutup toko di malam hari, gulir layar kasir ke bagian paling bawah dan tekan tombol biru **Lihat & Simpan Rekap Hari Ini**.
2. Layar akan menampilkan total jumlah transaksi dan total uang omzet yang terkumpul hari itu.
3. Buka folder `Download/kasir-md/laporan/`, ambil file **`rekap_YYYYMMDD.md`** hari ini, lalu kirimkan melalui WhatsApp kepada pemilik toko sebagai laporan tutup buku.

---

## 🏷️ Bagian 4: Cara Mengubah Harga atau Menambah Barang Baru

Pemilik toko tidak perlu mengubah kode aplikasi untuk memperbarui harga:
1. Buka aplikasi catatan teks biasa di HP atau tablet.
2. Buat file baru dengan format nama urutan tanggal hari ini, contoh: **`harga_2026_11_15.md`**.
3. Tulis daftar perubahan harga atau barang baru menggunakan format tabel seperti contoh ini:
   ```markdown

   | Kode | Nama Barang | Harga |
   | :--- | :--- | :--- |
   | BRG01 | Kopi Hitam | 7000 |
   | BRG05 | Es Jeruk | 6000 |
   ```
4. Simpan file tersebut ke dalam folder **`Download/kasir-md/data/`**.
5. Muat ulang (*Refresh*) halaman kasir di browser, dan harga baru akan langsung berlaku.
