from utils import spasi_ke_tagar


def putar(matrix):
    rotated_matrix = [
        [matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))
    ]
    return rotated_matrix


def tts_validation(matrix, strict=False, daftar_kata: list = []):
    to_hash = spasi_ke_tagar.replace_space_with_hash
    matrix = to_hash(matrix)

    def get_words(matrix, rotated=0):
        result = []
        matrix = matrix if rotated == 0 else putar(matrix)
        for row in matrix:
            joined = "".join(row)
            words = joined.split("#")
            words = [word for word in words if (word != "" and len(word) > 1)]
            if len(words) > 0:
                for word in words:
                    result.append(word)
        return result

    match_words = get_words(matrix) + get_words(matrix, rotated=1)
    input = set(daftar_kata)
    output = set(match_words)
    cocok = input == output
    if not strict:
        if not cocok:
            recheck = True
            for out in output:
                if out not in input:
                    recheck = False
            return recheck, match_words
    return cocok, match_words
