# Market Research & Idea Generator (Streamlit App)

Aplikasi ini membantu Anda melakukan riset pasar, menghasilkan ide produk/layanan baru, membandingkan ide berdasarkan kriteria, dan memvisualisasikan hasil perbandingan secara interaktif dengan bantuan AI (OpenRouter).

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

## Cara Menggunakan

1. **Siapkan API Key OpenRouter**
   - Daftar gratis di [OpenRouter.ai](https://openrouter.ai) dan dapatkan API Key.
   - Masukkan API Key di sidebar aplikasi.

2. **Input Data Riset Pasar**
   - Isi segmen pasar, masalah konsumen, tren, dan kompetitor di Tab "Generator Ide".
   - (Opsional) Tambahkan kriteria perbandingan.
   - Klik "Hasilkan Ide & Analisis".

3. **Bandingkan Ide**
   - Pindah ke Tab "Perbandingan Hasil".
   - Pilih minimal 2 ide, klik "Bandingkan Ide".

4. **Lihat Visualisasi**
   - Tab "Visualisasi Perbandingan Skor Ide" akan aktif setelah perbandingan.
   - Lihat bar chart dan kesimpulan otomatis.

5. **Simulasi BEP**
   - Gunakan sidebar untuk menghitung estimasi BEP.

## Penggunaan

Aplikasi ini cocok digunakan oleh:
- Mahasiswa, pelaku startup, UMKM, atau siapa saja yang ingin mencari ide bisnis berbasis data dan AI.
- Tim riset pasar yang ingin membandingkan beberapa ide secara objektif dan cepat.
- Siapa saja yang ingin melakukan simulasi BEP dan analisis SWOT secara otomatis.

Cukup masukkan data riset pasar, generate ide, bandingkan, dan dapatkan visualisasi serta insight secara instan!

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

## Instalasi & Menjalankan

1. Pastikan Python 3.8+ sudah terinstall.
2. Install dependencies:
   ```bash
   pip install streamlit requests pandas matplotlib numpy
   ```
3. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```

## Catatan
- Aplikasi ini menggunakan API OpenRouter (mirip ChatGPT) untuk menghasilkan ide dan analisis.
- Tidak menyimpan data pengguna.
- Untuk hasil terbaik, gunakan input yang spesifik dan jelas.

## Lisensi
MIT License

---

**Dibuat untuk pembelajaran dan eksplorasi AI di bidang market research dan ideasi produk.**
