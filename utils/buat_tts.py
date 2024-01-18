import random
import heapq
import itertools
from utils.hitung_biaya import hitung_biaya


def buat_teka_teki_silang(daftar_kata, checked_order=[]):
    # Langkah 1: Urutkan daftar kata berdasarkan panjang kata secara descending
    daftar_kata.sort(key=len, reverse=True)

    # Langkah 2: Hitung maksimum baris dan kolom untuk matriks
    maksimum_baris = len(daftar_kata[0]) * len(daftar_kata)
    maksimum_kolom = maksimum_baris

    # Inisialisasi matriks dengan spasi
    matriks = [[" " for _ in range(maksimum_kolom)] for _ in range(maksimum_baris)]

    # Tentukan indeks awal untuk meletakkan kata pertama di tengah
    indeks_baris = maksimum_baris // 2
    indeks_kolom = (maksimum_kolom - len(daftar_kata[0])) // 2

    # Langkah 3: Generate kemungkinan urutan kata
    possible_order = list(itertools.permutations(daftar_kata))
    possible_order = [x for x in possible_order if x not in checked_order]

    # Pilih urutan kata secara acak jika ada yang tersisa
    if len(possible_order) > 0:
        random_int_max = len(possible_order) - 1
        random_order_int = random.randint(0, random_int_max)
        daftar_kata = list(possible_order[random_order_int])

    # Letakkan kata pertama di matriks
    for i in range(len(daftar_kata[0])):
        matriks[indeks_baris][indeks_kolom + i] = daftar_kata[0][i]

    # if random.choice([True, False]):  # Ini akan menghasilkan True atau False secara acak
    #     # Letakkan kata pertama secara horizontal
    #     for i in range(len(daftar_kata[0])):
    #         matriks[indeks_baris][indeks_kolom + i] = daftar_kata[0][i]
    # else:
    #     # Letakkan kata pertama secara vertikal
    #     for i in range(len(daftar_kata[0])):
    #         matriks[indeks_baris + i][indeks_kolom] = daftar_kata[0][i]

    # Inisialisasi antrian prioritas untuk pencarian kata
    antrian = []
    heapq.heappush(antrian, (0, matriks, 1))
    jumlah_kata = 1

    # Langkah 4: Pencarian kata-kata berikutnya
    while antrian and jumlah_kata < len(daftar_kata):
        biaya, matriks, indeks = heapq.heappop(antrian)
        for k in range(len(daftar_kata[indeks])):
            karakter = daftar_kata[indeks][k]
            for baris in range(maksimum_baris):
                for m in range(maksimum_kolom):
                    if matriks[baris][m] == karakter:
                        bisa = True
                        for n in range(len(daftar_kata[indeks])):
                            if n != k and (
                                baris - k + n < 0
                                or baris - k + n >= maksimum_baris
                                or matriks[baris - k + n][m] != " "
                            ):
                                bisa = False
                                break
                        if bisa:
                            # Buat matriks baru jika kata dapat ditempatkan
                            matriks_baru = [baris[:] for baris in matriks]
                            for n in range(len(daftar_kata[indeks])):
                                matriks_baru[baris - k + n][m] = daftar_kata[indeks][n]
                            biaya_baru = hitung_biaya(
                                matriks_baru, maksimum_baris, maksimum_kolom
                            )
                            heapq.heappush(
                                antrian, (biaya_baru, matriks_baru, indeks + 1)
                            )
                        bisa = True
                        for n in range(len(daftar_kata[indeks])):
                            if n != k and (
                                m - k + n < 0
                                or m - k + n >= maksimum_kolom
                                or matriks[baris][m - k + n] != " "
                            ):
                                bisa = False
                                break
                        if bisa:
                            # Buat matriks baru jika kata dapat ditempatkan
                            matriks_baru = [baris[:] for baris in matriks]
                            for n in range(len(daftar_kata[indeks])):
                                matriks_baru[baris][m - k + n] = daftar_kata[indeks][n]
                            biaya_baru = hitung_biaya(
                                matriks_baru, maksimum_baris, maksimum_kolom
                            )
                            heapq.heappush(
                                antrian, (biaya_baru, matriks_baru, indeks + 1)
                            )
        jumlah_kata += 1

    # Langkah 5: Handle jika tidak ada solusi
    if not antrian:
        return "ERROR_N", daftar_kata

    # Pilih solusi terbaik dari antrian
    biaya, matriks, indeks = heapq.heappop(antrian)

    # Temukan batas atas, batas bawah, kolom kiri, dan kolom kanan dari matriks
    baris_atas, baris_bawah, kolom_kiri, kolom_kanan = -1, -1, -1, -1
    for baris in range(maksimum_baris):
        if any(matriks[baris][m] != " " for m in range(maksimum_kolom)):
            baris_bawah = baris
            if baris_atas == -1:
                baris_atas = baris
    for m in range(maksimum_kolom):
        if any(matriks[baris][m] != " " for baris in range(maksimum_baris)):
            kolom_kanan = m
            if kolom_kiri == -1:
                kolom_kiri = m

    # Potong matriks sesuai dengan batasan atas, bawah, kiri, dan kanan
    matriks_dipotong = [
        baris[kolom_kiri : kolom_kanan + 1]
        for baris in matriks[baris_atas : baris_bawah + 1]
    ]

    # Mengembalikan matriks hasil dan daftar kata yang digunakan
    return matriks_dipotong, daftar_kata
