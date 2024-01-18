from utils import (
    hitung_biaya,
    validasi_tts,
    cetak_papan,
    spasi_ke_tagar,
    buat_tts,
    cari_kata,
    buat_anotasi,
)
import math


class TTS:
    def __init__(self, input_kata):
        self.hb = hitung_biaya.hitung_biaya
        self.vt = validasi_tts.tts_validation
        self.cp = cetak_papan.cetakPapanHTML
        self.skt = spasi_ke_tagar.replace_space_with_hash
        self.buat_tts = buat_tts.buat_teka_teki_silang
        self.input_kata = input_kata
        self.cari = cari_kata.find_words
        self.anotasi = buat_anotasi.anotasi

    # Contoh penggunaan
    def buat(self):
        # copy input_kata to daftar_kata
        daftar_kata = self.input_kata.copy()
        daftar_kata = [x.upper() for x in daftar_kata]

        iterasi = 1
        max_iterasi = math.factorial(len(daftar_kata))
        daftar_urutan = []
        while iterasi <= max_iterasi:
            hasil_teka_teki, dicek = self.buat_tts(daftar_kata, daftar_urutan)
            daftar_urutan.append(tuple(dicek))
            tts_valid, match_words = self.vt(
                hasil_teka_teki, True, daftar_kata=[a.upper() for a in daftar_kata]
            )
            if tts_valid:
                break
            hasil_teka_teki = None
            iterasi += 1

        if hasil_teka_teki:
            return hasil_teka_teki
        else:
            return None

    def cetak(self, matrix=None):
        tts = self.buat() if not matrix else matrix
        if tts:
            html_papan = self.cp(tts)
            return html_papan
        else:
            return None

    def cari_kata(self, matrix=None):
        tts = self.buat() if not matrix else matrix
        if tts:
            results = self.cari(tts)
            return results
        else:
            return None

    def anotasi(self, matrix=None):
        tts = self.buat() if not matrix else matrix
        if tts:
            anotasi = self.anotasi(tts)
            return anotasi
        else:
            return None
