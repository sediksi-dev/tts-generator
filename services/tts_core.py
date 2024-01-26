import random
from typing import List

from services.logic.helper_functions import (
    rotate_matrix,
    find_matrix_bounds,
    change_blanks_cell,
)
from services.logic.core_functions import (
    place_first_word,
    find_match_patterns,
    generate_matrix,
)
from services.tts_helper import TTS_Helper


class TTS_Core(TTS_Helper):
    def __init__(self, max_tries=1000):
        super().__init__()
        self.__stop = False
        self.__max_tries = max_tries
        self.__all_words: List[str] = None
        self.__current_matrix: List[List[str]] = None
        self.__remaining_words: List[str] = None
        self.__best_trying = 0
        self.__best_matrix = None

    @property  # Getter method: Mengambil nilai dari property `all_words`
    def all_words(self):
        return self.__all_words

    @all_words.deleter  # Deleter method: Menghapus nilai dari property `all_words`
    def all_words(self):
        del self.__all_words

    @property  # Getter method: Mengambil nilai dari property `current_matrix`
    def current_matrix(self):
        return self.__current_matrix

    @property  # Getter method: Mengambil nilai dari property `best_matrix`
    def best_matrix(self):
        return self.__best_matrix

    @property  # Getter method: Mengambil nilai dari property `remaining_words`
    def remaining_words(self):
        return self.__remaining_words

    @property  # Getter method: Mengambil nilai dari property `added_words`
    def added_words(self):
        return [w for w in self.all_words if w not in self.remaining_words]

    # Mengurangi nilai dari property `max_tries` sebanyak 1
    def __decrease_max_tries(self):
        while self.__max_tries > 0:
            self.__max_tries -= 1
            return
        self.__stop = True

    # Fungsi untuk mengubah nilai dari property `all_words` dan `remaining_words` menjadi `words`
    def _set_words(self, words):
        self.__all_words = words
        self.__remaining_words = words

    # Fungsi untuk mengubah nilai dari property `remaining_words` menjadi `words`
    # Fungsi ini juga mengubah nilai dari property `best_trying` jika `len(self.added_words) > self.__best_trying`
    def __modify_remaining_words(self, words):
        if self.__remaining_words is not None:
            self.__remaining_words = words

        if len(self.added_words) > self.__best_trying:
            self.__best_trying += len(self.added_words)

    # Fungsi untuk mengubah nilai dari property `current_matrix` menjadi `None`
    def __reset_matrix(self):
        self.__current_matrix = None

    # Fungsi untuk mengubah nilai dari property `current_matrix` menjadi `matrix`
    # Fungsi ini juga mengubah nilai dari property `best_matrix` jika `len(self.added_words) >= self.__best_trying`
    def __update_current_matrix(self, matrix):
        self.__current_matrix = matrix
        if len(self.added_words) >= self.__best_trying:
            self.__best_matrix = matrix

    # Membuat matriks TTS paling tepat dari input kata yang telah ditentukan
    def _create_tts(self, separator=" "):
        """
        Membuat matriks TTS paling tepat dari input kata yang telah ditentukan
        :param words: Kata-kata yang akan dibuat matriksnya
        :param kwargs: Keyword arguments
        :key shuffled: Apakah kata-kata yang akan dibuat matriksnya diacak
        :key separator: Karakter yang akan digunakan sebagai pengganti karakter kosong
        :return: Matriks TTS yang telah dibuat atau None jika gagal
        """
        words = self.__all_words
        self.__modify_remaining_words(words)
        self.__reset_matrix()
        self._set_start()
        self._logging("Membuat matriks TTS ...", key="initialization")

        if len(words) == 0:
            return None

        matrix = self._generate(words)

        if matrix is None:
            return None

        top, bottom, left, right = find_matrix_bounds(matrix)
        # Potong matriks sesuai batas
        matrix = [row[left : right + 1] for row in matrix[top : bottom + 1]]

        row, col = len(matrix), len(matrix[0])
        if row > col:
            matrix = rotate_matrix(matrix)
            row, col = len(matrix), len(matrix[0])
        matrix = change_blanks_cell(matrix, to=separator)
        self._set_end()
        self.__update_current_matrix(matrix)
        return matrix

    # Menempatkan kata pertama yang belum digunakan dalam matriks TTS
    def _get_first_matrix(self, words, used_words):
        """
        Membuat matriks TTS dari kata pertama yang belum digunakan
        :param words: Kata-kata yang akan dibuat matriksnya
        :param used_words: Kata-kata yang telah digunakan
        :return: Kata pertama yang belum digunakan dan matriks TTS yang telah dibuat
        """
        self._logging("Menempatkan kata pertama ...", key="first_word")
        if len(words) == 0 or len(words) == len(used_words):
            self._logging(
                "Tidak ada kata yang tersedia untuk menempatkan kata pertama.",
                state="warning",
            )  # Logging
            return None, None

        # Memilih kata pertama yang belum digunakan
        word = next((w for w in words if w not in used_words), None)
        if word is None:
            return None, None

        matrix = place_first_word(word, words, doubled_matrix=False)

        if matrix is None:
            return None, None

        self.__update_current_matrix(matrix)
        return word, matrix

    # Memilih kombinasi kata untuk menempatkan kata pertama yang belum dicoba dalam matriks TTS
    # Fungsi ini akan berjalan secara rekursif jika kata pertama yang dicoba tidak dapat menemukan pola yang cocok
    def _generate(self, words, used_words=None):
        """
        Membuat matriks TTS dari kata-kata yang telah ditentukan
        :param words: Kata-kata yang akan dibuat matriksnya
        :param used_words: Kata-kata yang telah digunakan
        :return: Matriks TTS yang telah dibuat atau None jika gagal
        """
        self._logging("Memilih kombinasi kata ...", key="generate")

        # Jika used_words belum ditentukan, gunakan list kosong
        if used_words is None:
            used_words = []

        # Mencari kata pertama yang belum digunakan dan membuat matriks TTS
        first_word, base_matrix = self._get_first_matrix(words, used_words)

        # Jika kata pertama atau matriks TTS tidak ditemukan, maka gagal
        if base_matrix is None:
            return None

        # Mencari kata yang tersisa
        remaining_words = [w for w in words if w != first_word]
        self.__modify_remaining_words(remaining_words)

        # Menempatkan kata yang tersisa dalam matrix
        matrix = self._place_word(remaining_words, base_matrix)

        # Jika gagal, coba lagi dengan kata pertama yang berbeda
        if matrix is None:
            if self.__stop:
                return None
            return self._generate(words, used_words + [first_word])

        # Jika berhasil, kembalikan matriks TTS yang telah dibuat
        self.__update_current_matrix(matrix)
        return matrix

    # Membuat semua kombinasi kata yang tersisa dalam matriks TTS yang telah dibuat secara rekursif
    # Fungsi ini menjalankan iterasi secara rekursif dengan memanggil fungsi `_create_matrix` dan `_place_word`
    # jika kata yang tersisa tidak dapat ditempatkan dalam matriks TTS
    def _place_word(self, words, matrix, used_words_order=None):
        """
        Fungsi rekursif untuk menempatkan kata-kata yang tersisa dalam matriks TTS
        :param words: Kata-kata yang tersisa
        :param matrix: Matriks TTS yang telah dibuat
        :param used_words_order: Kombinasi kata yang telah dicoba
        :return: Matriks TTS yang telah dibuat atau None jika gagal
        """
        self._logging("Menempatkan kata ...", key="placing")

        if used_words_order is None:
            used_words_order = []

        if len(words) == 0:
            return matrix

        words_order = self._get_all_combinations(words)
        filtered_words_order = [w for w in words_order if w not in used_words_order]

        if len(filtered_words_order) == 0:
            return None

        for chosen_words_order in filtered_words_order:
            word = chosen_words_order[0]
            patterns = find_match_patterns(word, matrix)

            if len(patterns) > 0:
                # Membuat matriks baru dengan memilih pola yang cocok
                new_matrix = self._create_matrix(word, matrix, patterns)
                if new_matrix is not None:
                    remaining_words = [w for w in words if w != word]
                    used_words_order.append(chosen_words_order)

                    # Lanjutkan secara rekursif dengan kata yang tersisa
                    next_matrix = self._place_word(
                        remaining_words, new_matrix, used_words_order
                    )
                    if next_matrix is not None:
                        self.__update_current_matrix(next_matrix)
                        return next_matrix

                    # Jika gagal, kembalikan `used_words_order` ke keadaan sebelumnya
                    used_words_order.pop()

        return None

    # Membuat semua kombinasi kata yang tersisa dalam matriks TTS yang telah dibuat secara rekursif
    # Fungsi ini menjalankan iterasi secara rekursif dengan memanggil fungsi `_create_matrix` dan `_place_word`
    def _create_matrix(self, word, base_matrix, patterns, used_patterns=None):
        """
        Membuat matriks TTS baru dengan memilih pola yang cocok
        :param word: Kata yang akan dimasukkan
        :param base_matrix: Matriks TTS yang telah dibuat
        :param patterns: Pola yang cocok
        :param all_words: Kata-kata yang akan dibuat matriksnya
        :param used_patterns: Pola yang telah dicoba
        :return: Matriks TTS yang telah dibuat atau None jika gagal
        """
        self._logging("Membuat matriks TTS ...", key="create_matrix")
        if self.__stop:
            return None

        all_words = self.__all_words
        if used_patterns is None:
            used_patterns = []

        choosen_pattern = self._select_pattern(patterns, used_patterns)

        if choosen_pattern is None:
            return None

        matrix = generate_matrix(word, base_matrix, choosen_pattern, all_words)

        if matrix is not None:
            self.__update_current_matrix(matrix)
            return matrix

        used_patterns.append(choosen_pattern)
        return self._create_matrix(word, base_matrix, patterns, used_patterns)

    # Memilih kombinasi kata yang tersisa dalam matriks TTS yang telah dibuat secara rekursif
    def _select_pattern(self, patterns, used_patterns=None):
        """
        Memilih pola yang cocok
        :param patterns: Pola yang cocok
        :param used_patterns: Pola yang telah dicoba
        :return: Pola yang cocok atau None jika tidak ada
        """
        self.__decrease_max_tries()

        self._logging("Memilih kombinasi kata ...", key="patterning")
        if used_patterns is None:
            used_patterns = []

        available_patterns = [p for p in patterns if p not in used_patterns]
        random.shuffle(available_patterns)

        for choosen_pattern in available_patterns:
            return choosen_pattern

        return None
