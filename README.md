# Market Research & Idea Generator (Streamlit App)

## Deskripsi Singkat
**Latar belakang**
Pelaku bisnis UMKM dan startup seringkali menghadapi tantangan dalam melakukan riset pasar yang efektif karena keterbatasan sumber daya dan waktu. Proses identifikasi segmen pasar, analisis pain point konsumen, hingga evaluasi ide bisnis membutuhkan waktu mingguan bahkan bulanan. Di sisi lain, akses terhadap alat analisis profesional seperti SWOT dan perhitungan kelayakan finansial (BEP) biasanya mahal dan kompleks. Kesenjangan ini menyebabkan banyak ide bisnis potensial tidak teruji secara memadai sebelum diluncurkan, berisiko tinggi terhadap kegagalan pasar.

**Tujuan Projek**
Aplikasi ini dikembangkan untuk memberikan solusi riset pasar terintegrasi berbasis AI yang cepat, akurat, dan terjangkau. Dimana aplikasi ini berfungsi untuk:

1. Memangkas waktu riset dari mingguan menjadi hitungan menit melalui generasi ide otomatis berdasarkan     input pasar

2. Menyederhanakan analisis kompetitif dengan perbandingan multi-kriteria dan visualisasi data intuitif

3. Memberikan simulasi kelayakan finansial instan melalui kalkulator BEP interaktif

4. Mendemokratisasi akses alat profesional bagi UMKM dan pemula dengan antarmuka sederhana

5. Dengan menggabungkan AI OpenRouter, analisis data Python, dan visualisasi Streamlit, proyek ini mentransformasi proses pengembangan ide bisnis dari yang bersifat spekulatif menjadi berbasis data terstruktur.

## Fitur Utama

1. **Generator Ide Produk/Layanan**
   - Masukkan segmen pasar, masalah konsumen, tren, dan kompetitor.
   - AI akan menghasilkan 3 ide lengkap beserta analisis pasar, strategi pemasaran, keunggulan, risiko, dan SWOT.

2. **Perbandingan Ide**
   - Pilih 2 atau lebih ide untuk dibandingkan berdasarkan kriteria (default: Potensi Pasar, Kesulitan Implementasi, Inovasi, Modal Awal, bisa ditambah sendiri).
   - AI memberikan skor (1-5) untuk tiap kriteria dan ide, serta ringkasan analisis.

3. **Visualisasi Skor Ide**
   - Tampilkan bar chart rata-rata skor tiap ide.
   - Kesimpulan otomatis: jika ada lebih dari satu ide dengan skor tertinggi, aplikasi memberi saran untuk analisis lebih lanjut.
   - Saran tambahan jika Anda menambahkan kriteria favorit.

4. **Simulasi Break Even Point (BEP)**
   - Hitung estimasi waktu balik modal berdasarkan input modal, biaya operasional, dan omzet bulanan.

5. **Personalisasi Tanya AI**
   - Tanyakan apa saja tentang ide yang dihasilkan, misal strategi pemasaran, estimasi modal, keunggulan, dsb.

## Kebutuhan Instalasi

Pastikan Anda sudah menginstall:
- Python 3.8 atau lebih baru
- Paket berikut:
  - streamlit
  - requests
  - pandas
  - matplotlib
  - numpy

Install semua paket dengan perintah:
```bash
pip install streamlit requests pandas matplotlib numpy
```

## Cara Menjalankan di Lokal

1. Pastikan Python 3.8+ sudah terinstall.
2. Install dependencies:
   ```bash
   pip install streamlit requests pandas matplotlib numpy
   ```
3. Jalankan aplikasi dengan perintah berikut di terminal:
   ```bash
   streamlit run app.py
   ```
4. Buka browser dan akses alamat yang muncul (biasanya http://localhost:8501)
5. Masukkan API Key OpenRouter di sidebar aplikasi.

## Penggunaan

Aplikasi ini cocok digunakan oleh:
- Mahasiswa, pelaku startup, UMKM, atau siapa saja yang ingin mencari ide bisnis berbasis data dan AI.
- Tim riset pasar yang ingin membandingkan beberapa ide secara objektif dan cepat.
- Siapa saja yang ingin melakukan simulasi BEP dan analisis SWOT secara otomatis.

Cukup masukkan data riset pasar, generate ide, bandingkan, dan dapatkan visualisasi serta insight secara instan!


## Catatan
- Aplikasi ini menggunakan API OpenRouter (mirip ChatGPT) untuk menghasilkan ide dan analisis.
- Tidak menyimpan data pengguna.
- Untuk hasil terbaik, gunakan input yang spesifik dan jelas.

## Lisensi
MIT License

---

**Dibuat untuk pembelajaran dan eksplorasi AI di bidang market research dan ideasi produk.**
