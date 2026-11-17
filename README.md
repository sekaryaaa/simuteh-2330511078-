# SIMUTEH – Computer Vision

Repositori ini berisi implementasi praktikum Computer Vision untuk pengolahan citra daun teh. Pengembangan mencakup tahapan praproses citra, deteksi tepi, serta analisis bercak menggunakan operasi morfologi.

## Struktur Proyek

```text
simuteh-2330511078/
├── data/
│   └── sintetis/
├── hasil/
│   ├── p5_tabel_tepi.csv
│   ├── p5_f1_kondisi.png
│   ├── p6_evaluasi_bercak.csv
│   ├── p6_eksperimen_se.csv
│   └── param_bercak.json
├── notebook/
│   ├── B1_Lingkungan.ipynb
│   ├── B5_tepi.ipynb
│   └── B6_morfologi.ipynb
└── src/
    ├── praproses.py
    ├── utils_tepi.py
    └── bercak.py
```

## Praktikum P5 – Deteksi Tepi

Praktikum P5 membahas penerapan dan evaluasi metode deteksi tepi pada citra daun teh. Pengujian dilakukan dengan membandingkan beberapa metode, yaitu Sobel, Prewitt, LoG, dan Canny.

Pengujian mencakup variasi kondisi citra, sumber citra, kanal warna, serta penggunaan citra mentah dan citra hasil praproses.

Hasil pengujian disimpan dalam:

- `p5_tabel_tepi.csv`: tabel hasil evaluasi yang terdiri dari 640 kombinasi pengujian.
- `p5_f1_kondisi.png`: visualisasi nilai F1-score berdasarkan kondisi pengujian.

Evaluasi menggunakan Precision (P), Recall (R), dan F1-score.

## Praktikum P6 – Morfologi dan Analisis Bercak

Praktikum P6 membahas penerapan operasi morfologi untuk membersihkan hasil deteksi bercak, menyaring objek berdasarkan karakteristiknya, serta mengukur persentase luas bercak pada daun.

Analisis dilakukan melalui tahapan:
1. Membuat mask area daun.
2. Membuat mask awal bercak.
3. Membersihkan hasil deteksi menggunakan operasi morfologi.
4. Mengukur dan menyaring objek bercak.
5. Menghitung persentase luas bercak terhadap luas daun.
6. Menentukan kelas kondisi daun menjadi Sehat, Ringan, atau Berat.

### Ringkasan Evaluasi

Evaluasi dilakukan terhadap 60 citra daun teh.

| Metrik | Hasil |
|---|---:|
| Jumlah citra | 60 |
| Akurasi klasifikasi | 88,3% |
| Jumlah prediksi benar | 53 |
| MAE persentase bercak | 0,582 |
| Korelasi persentase prediksi dan acuan | 0,954 |

Hasil evaluasi disimpan dalam:
- `p6_evaluasi_bercak.csv`: hasil pengukuran dan klasifikasi setiap citra.
- `p6_eksperimen_se.csv`: hasil eksperimen variasi structuring element.
- `param_bercak.json`: parameter yang digunakan dalam analisis bercak.

## Cara Menggunakan Modul Analisis Daun

Modul `bercak.py` menyediakan fungsi `analisis_daun()` untuk melakukan analisis bercak pada citra BGR yang telah melalui tahap praproses.

Contoh penggunaan:

```python
import bercak

# img_praproses merupakan citra BGR hasil praproses
hasil = bercak.analisis_daun(img_praproses)

print("Jumlah bercak:", hasil["jumlah_bercak"])
print("Persentase bercak:", hasil["persen_bercak"], "%")
print("Kelas kondisi:", hasil["kelas"])
```

Fungsi `analisis_daun()` menghasilkan kamus dengan informasi berikut:

| Key | Keterangan |
|---|---|
| `mask_daun` | Mask area daun |
| `mask_bercak` | Mask hasil deteksi bercak |
| `jumlah_bercak` | Jumlah objek bercak yang terdeteksi |
| `persen_bercak` | Persentase luas bercak terhadap luas daun |
| `kelas` | Kelas kondisi daun |
| `bercak` | Daftar objek bercak hasil pengukuran |

Parameter analisis dapat disesuaikan melalui argumen `p`. Jika tidak diberikan, fungsi menggunakan parameter bawaan dari modul.

## Reproduksibilitas

Untuk menjalankan ulang eksperimen:

1. Buka notebook `B5_tepi.ipynb` dan `B6_morfologi.ipynb` melalui Google Colab.
2. Pastikan Google Drive sudah terhubung dan direktori proyek tersedia.
3. Jalankan setiap notebook menggunakan **Restart & Run All**.
4. Periksa hasil keluaran pada direktori `hasil/`.

Parameter bawaan praproses tersedia pada modul `praproses.py`, sedangkan parameter analisis bercak disimpan dalam `hasil/param_bercak.json`.


