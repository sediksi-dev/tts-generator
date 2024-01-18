import string


def anotasi(matrix):
    """
    Membuat anotasi untuk papan TTS.
    Tandai setiap sel yang kosong dengan kombinasi huruf dan angka berdasarkan baris dan kolomnya.
    Contoh: A1, A2, A3, dst.
    """

    # Membuat daftar huruf
    alphabet = list(string.ascii_uppercase)
    # Membuat daftar angka
    numbers = list(range(1, len(matrix) + 1))

    # buat daftar anotasi berdasarkan matrix dua dimensi
    results = []
    for i, row in enumerate(matrix):
        cols = []
        for j, col in enumerate(row):
            code = f"{alphabet[j]}{str(numbers[i])}"
            val = matrix[i][j]
            empty = val == " "
            cols.append({"code": code, "value": val, "empty": empty})
        results.append(cols)

    return results
