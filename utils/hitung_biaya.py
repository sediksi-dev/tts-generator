def hitung_biaya(matriks, maksimum_baris, maksimum_kolom):
    # Inisialisasi biaya dengan 0
    biaya = 0
    # Menghitung jumlah kata yang berhimpitan
    jumlah_himpitan = 0
    for baris in range(maksimum_baris):
        for m in range(maksimum_kolom):
            if matriks[baris][m] != " ":
                # Cek apakah ada karakter di sebelah kiri atau kanan
                if (m > 0 and matriks[baris][m - 1] != " ") or (
                    m < maksimum_kolom - 1 and matriks[baris][m + 1] != " "
                ):
                    # Cek apakah ada karakter di atas atau bawah
                    if (baris > 0 and matriks[baris - 1][m] != " ") or (
                        baris < maksimum_baris - 1 and matriks[baris + 1][m] != " "
                    ):
                        # Jika ada, berarti ada himpitan
                        jumlah_himpitan += 1
    # Menambahkan jumlah himpitan ke biaya
    biaya += jumlah_himpitan
    # Menghitung jumlah ruang kosong yang tersisa
    jumlah_kosong = 0
    for baris in range(maksimum_baris):
        for m in range(maksimum_kolom):
            if matriks[baris][m] == " ":
                jumlah_kosong += 1
    # Menambahkan jumlah kosong ke biaya
    biaya += jumlah_kosong
    # Mengembalikan biaya
    return biaya
