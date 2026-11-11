#!/data/data/com.termux/files/usr/bin/bash

# Pindah ke folder kasir-md di penyimpanan internal Android
cd /storage/emulated/0/Download/kasir-md

# Jalankan server Python di latar belakang
python kasir_web.py &

# Tunggu 1 detik agar server siap, lalu buka browser Chrome otomatis
sleep 1
am start -a android.intent.action.VIEW -d http://localhost:8080
