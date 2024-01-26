import re


def add_word(words, word, cells, direction):
    if len(word) > 1:
        words.append(
            {"word": word, "cells": cells, "direction": direction, "clue": "###"}
        )


def custom_order(key):
    match = re.match(r"([a-zA-Z]+)([0-9]+)", key)
    return (int(match.group(2)), match.group(1))


def identify_words(annotated_matrix):
    horizontal_words, vertical_words = [], []

    for row in annotated_matrix:
        word, cells = "", []
        for cell in row:
            if not cell["empty"]:
                word += cell["value"]
                cells.append(cell["code"])
            else:
                add_word(horizontal_words, word, cells, "mendatar")
                word, cells = "", []
        add_word(horizontal_words, word, cells, "mendatar")

    for col in range(len(annotated_matrix[0])):
        word, cells = "", []
        for row in annotated_matrix:
            cell = row[col]
            if not cell["empty"]:
                word += cell["value"]
                cells.append(cell["code"])
            else:
                add_word(vertical_words, word, cells, "menurun")
                word, cells = "", []
        add_word(vertical_words, word, cells, "menurun")

    results = horizontal_words + vertical_words
    results.sort(key=lambda x: custom_order(x["cells"][0]))

    return results
