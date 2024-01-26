from .rotate import rotate


def get_words(matrix):
    """
    Mendapatkan kata-kata dari matriks yang diberikan.
    :param matrix: Matriks TTS.
    :param rotated: Indikator apakah matriks diputar.
    :return: Daftar kata yang ditemukan.
    """
    result = []
    for row in matrix:
        words = "".join(row).split("#")
        words = [word for word in words if (word != "" and len(word) > 1)]
        if len(words) > 0:
            for word in words:
                result.append(word)

    for row in rotate(matrix):
        words = "".join(row).split("#")
        words = [word for word in words if (word != "" and len(word) > 1)]
        if len(words) > 0:
            for word in words:
                result.append(word)
    return result
