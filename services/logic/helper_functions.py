def generate_styles():
    styles = """
    <style>
    .row {
        display: flex;
        flex-direction: row;
    }
    .cell {
        width: 30px;
        height: 30px;
        border: 1px solid black;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #fff;
        color: #000;
    }
    .empty {
        background-color: #000;
        color: #fff;
    }
    </style>
    """
    return styles


def display_matrix(matrix, blanks="#"):
    if matrix is None or len(matrix) == 0:
        return "Matrix is empty"

    styles = generate_styles()
    copied_matrix = matrix.copy()
    dim = len(copied_matrix[0])
    nmbr = [str(x % 10) for x in range(0, dim)]
    hsep = ["-" for x in range(0, (dim))]
    results = ""
    results += f"X | {' '.join(nmbr)}\n"
    results += f"- | {' '.join(hsep)}\n"
    for idx, row in enumerate(copied_matrix):
        results += str(idx % 10) + " | "
        results += " ".join(row)
        results += "\n"

    # matrix to html
    html = "<div>"
    for idx, row in enumerate(copied_matrix):
        html += "<div class='row'>"
        for char in row:
            if char == blanks:
                html += f"<div class='cell empty'>{char}</div>"
            else:
                html += f"<div class='cell'>{char}</div>"
        html += "</div>"
    html += "</div>"

    html += styles
    return html


def max_matrix(words, doubled=False):
    words = [x.upper() for x in words]
    max_len = len("".join(words)) * 2 if doubled else len("".join(words))
    matrix = []
    for i in range(max_len):
        row = []
        for d in range(max_len):
            row.append("#")
        matrix.append(row)
    return matrix


def remove_duplicates(dicts):
    seen = set()
    new_dicts = []
    for d in dicts:
        identifier = (d.get("pattern"), d.get("coordinates"))
        if identifier not in seen:
            seen.add(identifier)
            new_dicts.append(d)
    return new_dicts


def find_possibility(word, matrix):
    length, start, pos = len(word), 0, []  # rules variables
    loop = len(matrix) - length + 1  # count looping for this matrix

    coordinates, hor, ver = [], [], []  # array wrapper for catch looping val
    blanks = "#" * length  # Used for filtering the match patterns

    # Function to filtering the all combination to fit the patterns
    def match_pattern(pattern, word):
        if len(pattern) != len(word):
            return False
        return all(p == w or p == "#" for p, w in zip(pattern, word))

    # Function to combine all coordinates
    def combine(a, b):
        r = []
        for ida, c in enumerate(a):
            s = []
            for idb, d in enumerate(b):
                coord = c, d
                s.append(coord)
            r.append(s)
        return r

    # find all of combination from a matrix, based on word lengths
    while start < loop:
        val = [x for x in range(0 + start, length + start)]
        pos.append(val)
        start += 1

    # change the combination to a coordinates
    for idx, row in enumerate(pos):
        for i in range(0, len(pos)):
            merged = combine(pos[idx], pos[i])
            for m in merged:
                coordinates.append(m)

    # Find the possibe patterns and add to hor, or ver container
    for coord in coordinates:
        char_h, char_v = [], []
        for c in coord:
            char_h.append(matrix[c[0]][c[1]])
            char_v.append(matrix[c[1]][c[0]])
        word_h = "".join(char_h)
        if blanks != word_h:
            hor.append({"pattern": word_h, "dir": "h", "coord": coord})

        word_v = "".join(char_v)
        if blanks != word_v:
            ver.append(
                {
                    "pattern": word_v,
                    "dir": "v",
                    "coord": [(c[1], c[0]) for c in coord],
                }
            )
    patterns = hor + ver
    # remove duplicate values
    patterns = remove_duplicates(patterns)

    # filter data based on words
    match_patterns = [d for d in patterns if match_pattern(d["pattern"], word)]
    return match_patterns


def rotate_matrix(matrix):
    # Menggunakan list comprehension untuk transpose matriks
    # dan membalik urutan setiap sub-list
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def rotate(matrix):
    """
    Memutar matriks 90 derajat ke kanan.
    :param matrix: Matriks yang akan diputar.
    :return: Matriks yang telah diputar.
    """
    rotated_matrix = []
    for col in range(len(matrix[0])):
        rotated_matrix.append([])
        for row in range(len(matrix)):
            rotated_matrix[col].append(matrix[row][col])
    return rotated_matrix


def get_words(matrix, rotated=0):
    """
    Mendapatkan kata-kata dari matriks yang diberikan.
    :param matrix: Matriks TTS.
    :param rotated: Indikator apakah matriks diputar.
    :return: Daftar kata yang ditemukan.
    """
    result = []
    matrix = matrix if rotated == 0 else rotate(matrix)
    for row in matrix:
        words = "".join(row).split("#")
        words = [word for word in words if (word != "" and len(word) > 1)]
        if len(words) > 0:
            for word in words:
                result.append(word)
    return result


def validation(matrix, word_list=[]):
    """
    Memvalidasi teka-teki silang berdasarkan daftar kata yang diberikan.
    :param matrix: Matriks TTS.
    :param word_list: Daftar kata untuk validasi.
    :return: Hasil validasi dan kata-kata yang ditemukan.
    """

    found_words = set(get_words(matrix) + get_words(matrix, rotated=1))
    input_words = set(word_list)
    matches = [w for w in found_words if w not in input_words]
    is_match = len(matches) == 0
    return is_match


def find_matrix_bounds(matrix):
    """
    Mencari batas atas, bawah, kiri, dan kanan dari matriks
    :param matrix: matriks yang akan dicari batasnya
    :return: batas atas, bawah, kiri, dan kanan dari matriks (tuple)
    """

    # Mencari batas atas, bawah, kiri, dan kanan dari matriks
    top, bottom, left, right = -1, -1, -1, -1
    for row in range(len(matrix)):
        if any(matrix[row][col] != "#" for col in range(len(matrix[0]))):
            bottom = row
            if top == -1:
                top = row
    for col in range(len(matrix[0])):
        if any(matrix[row][col] != "#" for row in range(len(matrix))):
            right = col
            if left == -1:
                left = col
    return top, bottom, left, right


def change_blanks_cell(matrix, to, of="#"):
    for rows in matrix:
        for idx, cell in enumerate(rows):
            if cell == of:
                rows[idx] = to

    return matrix
