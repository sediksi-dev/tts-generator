import re


def urutan_kustom(kunci):
    # Mencocokkan huruf dan angka
    cocokan = re.match(r"([a-zA-Z]+)([0-9]+)", kunci)
    huruf, angka = cocokan.groups()
    return (int(angka), huruf)


# Mencari kata-kata mendatar dan menurun
def find_words(matrix):
    horizontal_words = []
    vertical_words = []

    # Pencarian kata mendatar
    for row in matrix:
        cells = []
        word = ""
        for cell in row:
            if not cell["empty"]:
                word += cell["value"]
                cells.append(cell["code"])
            else:
                if len(word) > 1:
                    horizontal_words.append(
                        {"word": word, "cells": cells, "to": "mendatar"}
                    )
                word = ""
        if len(word) > 1:
            horizontal_words.append({"word": word, "cells": cells, "to": "mendatar"})

    # Pencarian kata menurun
    for col in range(len(matrix[0])):
        cells = []
        word = ""
        for row in range(len(matrix)):
            cell = matrix[row][col]
            if not cell["empty"]:
                word += cell["value"]
                cells.append(cell["code"])
            else:
                if len(word) > 1:
                    vertical_words.append(
                        {"word": word, "cells": cells, "to": "menurun"}
                    )
                word = ""
        if len(word) > 1:
            vertical_words.append({"word": word, "cells": cells, "to": "menurun"})
    results = horizontal_words + vertical_words

    # Sort results by first value of "cells" key
    results = sorted(results, key=lambda x: urutan_kustom(x["cells"][0]))
    # Add group number to results
    for i, result in enumerate(results):
        results[i]["group"] = i + 1

    results = sorted(results, key=lambda x: x["group"])

    # add clues as key with empty value
    for result in results:
        result["clue"] = "###"

    return results
