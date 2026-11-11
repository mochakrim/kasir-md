from datetime import datetime
import glob
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

FOLDER_DASAR = os.path.dirname(os.path.abspath(__file__))


def muat_database_md():
  database = {}
  pola_file = os.path.join(FOLDER_DASAR, "data", "*.md")
  for file_path in sorted(glob.glob(pola_file)):
    with open(file_path, "r", encoding="utf-8") as f:
      for baris in f:
        baris = baris.strip()
        if (
            not baris.startswith("|")
            or "---" in baris
            or "Kode" in baris
        ):
          continue
        kolom = [k.strip() for k in baris.split("|") if k.strip()]
        if len(kolom) >= 3:
          try:
            kode = kolom[0]
            nama = kolom[1]
            harga = int(kolom[2].replace(".", "").replace(",", ""))
            database[kode] = {"kode": kode, "nama": nama, "harga": harga}
          except ValueError:
            continue
  return list(database.values())


def simpan_struk_md(keranjang, total_harga, tunai, kembalian):
  folder_struk = os.path.join(FOLDER_DASAR, "struk")
  os.makedirs(folder_struk, exist_ok=True)
  waktu = datetime.now()
  id_trx = waktu.strftime("%Y%m%d_%H%M%S")
  tgl_cetak = waktu.strftime("%d-%m-%Y %H:%M")

  baris = [
      "================================",
      "          KASIR TOKO            ",
      "================================",
      f"No  : TRX-{id_trx}",
      f"Tgl : {tgl_cetak}",
      "--------------------------------",
  ]
  for item in keranjang:
    nama = item["nama"][:18].ljust(18)
    harga = f"Rp {item['harga']:,}".rjust(13)
    baris.append(f"{nama} {harga}")

  baris.extend([
      "--------------------------------",
      f"TOTAL   : Rp {total_harga:,}".rjust(32),
      f"TUNAI   : Rp {tunai:,}".rjust(32),
      f"KEMBALI : Rp {kembalian:,}".rjust(32),
      "================================",
      "         Terima Kasih           ",
      "================================",
  ])
  teks_struk = "\n".join(baris)

  nama_file = os.path.join(folder_struk, f"struk_{id_trx}.md")
  with open(nama_file, "w", encoding="utf-8") as f:
    f.write("```text\n" + teks_struk + "\n```\n")
  return teks_struk, f"struk/struk_{id_trx}.md"


def buat_rekap_harian_md():
  waktu = datetime.now()
  kode_hari_ini = waktu.strftime("%Y%m%d")
  tgl_tampil = waktu.strftime("%d-%m-%Y")
  pola_struk = os.path.join(
      FOLDER_DASAR, "struk", f"struk_{kode_hari_ini}_*.md"
  )
  daftar_struk = sorted(glob.glob(pola_struk))

  total_omzet = 0
  rincian_trx = []
  for file_path in daftar_struk:
    nama_file = os.path.basename(file_path)
    nominal_trx = 0
    with open(file_path, "r", encoding="utf-8") as f:
      for baris in f:
        if "TOTAL" in baris and "Rp" in baris:
          try:
            nominal_trx = int(baris.split("Rp")[1].strip().replace(",", ""))
            total_omzet += nominal_trx
          except ValueError:
            pass
    jam = nama_file.replace(f"struk_{kode_hari_ini}_", "").replace(".md", "")
    jam_fmt = f"{jam[:2]}:{jam[2:4]}:{jam[4:6]}" if len(jam) == 6 else jam
    rincian_trx.append(f"| {jam_fmt} | {nama_file} | Rp {nominal_trx:,} |")

  folder_laporan = os.path.join(FOLDER_DASAR, "laporan")
  os.makedirs(folder_laporan, exist_ok=True)
  file_rekap = os.path.join(folder_laporan, f"rekap_{kode_hari_ini}.md")

  isi_md = [
      f"# REKAP PENJUALAN HARIAN ({tgl_tampil})",
      "",
      f"- **Jumlah Transaksi:** {len(daftar_struk)} transaksi",
      f"- **Total Omzet Hari Ini:** Rp {total_omzet:,}",
      "",
      "| Waktu | File Struk | Nominal |",
      "| :--- | :--- | :--- |",
  ]
  isi_md.extend(
      rincian_trx if rincian_trx else ["| - | Belum ada transaksi | Rp 0 |"]
  )

  teks_laporan = "\n".join(isi_md)
  with open(file_rekap, "w", encoding="utf-8") as f:
    f.write(teks_laporan + "\n")

  return {
      "tanggal": tgl_tampil,
      "jumlah_trx": len(daftar_struk),
      "total_omzet": total_omzet,
      "teks_laporan": teks_laporan,
      "file": f"laporan/rekap_{kode_hari_ini}.md",
  }


class KasirHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    if self.path == "/":
      self.send_response(200)
      self.send_header("Content-type", "text/html; charset=utf-8")
      self.end_headers()
      with open(os.path.join(FOLDER_DASAR, "index.html"), "rb") as f:
        self.wfile.write(f.read())
    elif self.path == "/api/produk":
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      self.wfile.write(json.dumps(muat_database_md()).encode("utf-8"))
    elif self.path == "/api/rekap":
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      self.wfile.write(json.dumps(buat_rekap_harian_md()).encode("utf-8"))

  def do_POST(self):
    if self.path == "/api/bayar":
      panjang = int(self.headers["Content-Length"])
      payload = json.loads(self.rfile.read(panjang).decode("utf-8"))
      teks_struk, nama_file = simpan_struk_md(
          payload["keranjang"],
          payload["total"],
          payload["tunai"],
          payload["kembalian"],
      )
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      self.wfile.write(
          json.dumps({"struk": teks_struk, "file": nama_file}).encode("utf-8")
      )


print(f"Berhasil membaca {len(muat_database_md())} barang dari folder data/")
print("Server berjalan! Buka Safari: http://localhost:8080")
HTTPServer(("0.0.0.0", 8080), KasirHandler).serve_forever()
