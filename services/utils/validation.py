from services.utils import get_words, replace_space_with_hash


def validation(matrix, strict=False, word_list=[]):
    """
    Memvalidasi teka-teki silang berdasarkan daftar kata yang diberikan.
    :param matrix: Matriks TTS.
    :param strict: Mode validasi ketat (True) atau tidak ketat (False).
    :param word_list: Daftar kata untuk validasi.
    :return: Hasil validasi dan kata-kata yang ditemukan.
    """
    matrix = replace_space_with_hash(matrix)

    found_words = set(get_words(matrix) + get_words(matrix, rotated=1))
    input_words = set(word_list)
    output = set(found_words)
    match = input_words == found_words
    # Jika tidak ketat, maka lakukan pengecekan lagi
    if not strict:
        if not match:
            recheck = True
            for out in output:
                if out not in input:
                    recheck = False
            return recheck, list(found_words)
    return match, list(found_words)
