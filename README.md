# Teka-Teki Silang Generator

Teka-Teki Silang Generator adalah aplikasi web yang memungkinkan pengguna untuk membuat teka-teki silang. Aplikasi ini dibangun menggunakan Python dan library Streamlit.

## Fitur

- Membuat papan teka-teki silang dari daftar kata yang diberikan.
- Menyediakan antarmuka pengguna yang ramah untuk menambah dan mengedit petunjuk teka-teki silang.
- Menampilkan papan teka-teki silang yang siap untuk dicetak atau diintegrasikan dalam media lain.

## Struktur Direktori

- `env`: Direktori untuk lingkungan virtual Python.
- `generator`: Modul yang berisi logika pembuatan teka-teki silang.
- `utils`: Kumpulan skrip bantuan untuk tugas-tugas seperti validasi dan pencarian kata.
- `app.py`: File utama yang menjalankan aplikasi web Streamlit.
- `papan_tts.png`: Contoh output papan teka-teki silang.
- `README.md`: File ini, yang memberikan informasi tentang proyek.
- `requirements.txt`: Daftar dependensi Python yang diperlukan untuk menjalankan aplikasi.

## Cara Menjalankan

Pastikan Anda telah menginstal Python dan pip. Kemudian, ikuti langkah-langkah berikut:

1. Klon repository ini.
2. Buat dan aktifkan lingkungan virtual (opsional tapi disarankan):
   ```
   python -m venv env
   source env/bin/activate  # Untuk Unix atau MacOS
   env\Scripts\activate  # Untuk Windows
   ```
3. Instal dependensi:
   ```
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi:
   ```
   streamlit run app.py
   ```

## Kontribusi

Kami menyambut kontribusi dari komunitas. Silakan fork repository ini dan kirimkan pull request Anda.

## Lisensi

[MIT](LICENSE)
