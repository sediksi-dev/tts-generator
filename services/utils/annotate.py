import string
import itertools


def annotate(matrix):
    """
    Membuat anotasi untuk matriks dua dimensi.
    :param matrix: Matriks dua dimensi yang akan diberi anotasi.
    :return: Matriks dua dimensi yang sudah diberi anotasi (list of lists of dicts).
    """

    # Membuat daftar huruf
    alphabet = list(string.ascii_uppercase)
    alphabet.extend(
        [
            f"{alphabet[i]}{alphabet[j]}"
            for i, j in itertools.product(range(len(alphabet)), repeat=2)
        ]
    )
    # Membuat daftar angka
    numbers = list(range(1, len(matrix) + 1))

    # Membuat daftar anotasi berdasarkan matrix dua dimensi
    annotated_matrix = []
    for i, row in enumerate(matrix):
        annotated_row = []
        for j, value in enumerate(row):
            code = f"{alphabet[j]}{numbers[i]}"
            empty = value == " "
            annotated_row.append({"code": code, "value": value, "empty": empty})
        annotated_matrix.append(annotated_row)
    return annotated_matrix
