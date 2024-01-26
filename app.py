import streamlit as st
import itertools
from joblib import Parallel, delayed


# import random
import time
import numpy as np

from services.logicv2.helper_functions import display_matrix
from services.logicv2.core_functions_old import (
    generate_patterns,
    generate_matrix_with_validation,
)
from services.logicv2.place_firstword import place_first
from helper.dev_tools import measure_execution_time


# from services.utils import validation
# from services.logicv2.helper_functions import max_matrix
def create_matrix(word, base_matrix, all_words):
    matrix = np.array(base_matrix)
    patterns = generate_patterns(word, matrix)
    if len(patterns) == 0:
        return False
    else:
        valid_matrix = generate_matrix_with_validation(
            word,
            matrix,
            patterns,
            all_words,
        )

        return valid_matrix


def process_word(word, matrix, words, all_words):
    new_matrix = create_matrix(word, matrix, all_words)
    if not new_matrix:
        # Jika tidak ada kombinasi yang valid, kembalikan None
        return None, None
    remaining_words = [w for w in words if w != word]
    return new_matrix, remaining_words


def process_combinations(matrix, words_order, first_word, all_words):
    combinations = get_all_combinations(matrix, words_order, all_words, [first_word])
    return combinations


def get_all_combinations(matrix, words, all_words, path=[]):
    if len(words) == 0:
        return [{"susunan": path, "matrix": matrix}]

    word = words[0]
    new_matrix, remaining_words = process_word(word, matrix, words, all_words)

    if new_matrix is None:
        # Tidak ada kombinasi yang valid
        return []

    combinations = []
    for nm in new_matrix:
        new_path = path + [word]
        combinations += get_all_combinations(nm, remaining_words, all_words, new_path)
    return combinations


def app(words):
    all_placed = place_first(words)
    if not all_placed:
        # Jika tidak ada tempat untuk memulai, kembalikan list kosong
        return []

    all_combinations = []
    for placed in all_placed:
        word = placed["word"]
        matrix = placed["results"]["matrix"]
        remaining_words = [w for w in words if w != word]
        remaining_words_order = itertools.permutations(remaining_words)
        for rw in remaining_words_order:
            combinations = get_all_combinations(matrix, rw, words, [word])
            if combinations:
                all_combinations += combinations

    return all_combinations


def app_parallel(words):
    all_placed = place_first(words)
    if not all_placed:
        return []

    tasks = []
    for placed in all_placed:
        word = placed["word"]
        matrix = placed["results"]["matrix"]
        remaining_words = [w for w in words if w != word]
        remaining_words_order = itertools.permutations(remaining_words)
        for rw in remaining_words_order:
            tasks.append((matrix, rw, word))

    # Menggunakan joblib untuk menjalankan tugas secara paralel
    all_combinations = Parallel(n_jobs=-1)(
        delayed(process_combinations)(matrix, rw, word, words)
        for matrix, rw, word in tasks
    )

    # Menggabungkan hasil
    combined_results = []
    for combination in all_combinations:
        if combination:
            combined_results.extend(combination)

    return combined_results


if __name__ == "__main__":
    if "btn_clicked" not in st.session_state:
        st.session_state.btn_clicked = False

    st.title("Beta Tes")
    st.markdown("## Menguji Fungsi-Fungsi Pada Logicv2")
    words_str = st.text_input(
        "Masukkan daftar kata yang akan dicari polanya. Pisahkan dengan koma (,).",
        key="words_str",
    )

    words = [x.strip().upper() for x in words_str.split(",")]
    # random.shuffle(words)
    btn = st.empty()

    def toggle_clicked():
        st.session_state.btn_clicked = not st.session_state.btn_clicked

    rerun = btn.button(
        "CARI POLA", on_click=toggle_clicked, disabled=st.session_state.btn_clicked
    )
    if rerun:
        time.sleep(3)
        toggle_clicked()
        st.rerun()

    duration, combinations = measure_execution_time(app_parallel, words)
    # duration, combinations = measure_execution_time(app, words)

    st.write("Waktu eksekusi paralel: {:.10f} detik".format(duration))
    st.write("Jumlah kombinasi: {}".format(len(combinations)))

    def displaying(combinations):
        for c in combinations:
            susunan_kata = "->".join(c["susunan"])
            st.write(f"Urutan kata: {susunan_kata}")
            st.write(display_matrix(c["matrix"]), unsafe_allow_html=True)

    displaying(combinations)
