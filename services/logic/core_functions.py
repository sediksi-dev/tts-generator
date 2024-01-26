import math
import numpy as np
from services.logic.helper_functions import max_matrix, validation


def place_first_word(word, words, doubled_matrix=False):
    matrix = max_matrix(words, doubled=doubled_matrix)
    dim_max = len(matrix)
    dim_is_odd = dim_max % 2 == 1
    char_count = len(word)
    char_is_odd = char_count % 2 == 1

    center = math.ceil(dim_max / 2) if dim_is_odd else dim_max / 2
    half_word = math.floor(char_count / 2) if char_is_odd else char_count / 2

    center_start = center - half_word - 1

    for idx, char in enumerate(list(word)):
        # jika horizontal col-nya tetap
        row = int(center - 1)
        col = int(center_start + idx)

        matrix[int(row)][int(col)] = char

    return matrix


# Function to filtering the all combination to fit the patterns
def match_pattern(pattern, string):
    if len(pattern) != len(string):
        return False

    for p, s in zip(pattern, string):
        if p != "#" and p != s:
            return False

    return True


def coord_to_pattern(coord: [[int, int]], dir, matrix):
    chars = []
    for c in coord:
        chars.append(matrix[c[0]][c[1]])
    pt = "".join(chars)
    return {
        "pattern": pt,
        "dir": dir,
        "coord": coord,
    }


# @title Cari pola yang memungkinkan
def find_match_patterns(word, matrix):
    if matrix is None:
        return []

    length, start, combinations = len(word), 0, []  # rules variables
    loop = len(matrix) - length + 1  # count looping for this matrix

    hor, ver = [], []  # array wrapper for catch looping val
    blanks = "#" * length  # Used for filtering the match patterns

    # find all of combination from a matrix, based on word lengths
    while start < loop:
        val = [x for x in range(0 + start, length + start)]
        combinations.append(val)
        start += 1

    for idx, rows in enumerate(matrix):
        # horizontal coordinates
        coord_h = [[[idx, x] for x in range(c[0], c[-1] + 1)] for c in combinations]
        coord_v = [[[x, idx] for x in range(c[0], c[-1] + 1)] for c in combinations]
        hor += [
            x
            for x in [coord_to_pattern(c, "h", matrix) for c in coord_h]
            if x["pattern"] != blanks
        ]
        ver += [
            x
            for x in [coord_to_pattern(c, "v", matrix) for c in coord_v]
            if x["pattern"] != blanks
        ]

    patterns = hor + ver
    match_patterns = [d for d in patterns if match_pattern(d["pattern"], word)]
    return match_patterns


# @title Membuat matrix dari pola yang memungkinkan
def generate_matrix(word, base_matrix, patterns, all_words):
    matrix = np.array(base_matrix.copy())
    chars = list(word)

    for idx, cr in enumerate(patterns["coord"]):
        matrix[cr[0]][cr[1]] = chars[idx]

    if validation(matrix, all_words):
        return matrix
    else:
        return None
