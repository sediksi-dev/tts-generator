from services.tts_core import TTS_Core
from services.utils import print_crosswords, annotate, identify_words, get_first_cells
from helper.sessions import Sessions


class TTS_Generator(TTS_Core, Sessions):
    def __init__(self):
        super().__init__()
        self.__input_words: str = None
        self.__tts_matrix = None
        self.__tts_annotation = None
        self.__tts_words = None
        self.__tts_printed = None
        self.__first_cells = None
        self.__separator = " "
        self.tts_name = {}

    @property
    def str_words(self):
        return self.__input_words

    @property
    def list_words(self):
        return self.all_words

    @property
    def __details(self):
        return {
            "matrix": self.__tts_matrix,
            "annotation": self.__tts_annotation,
            "words": self.__tts_words,
            "printed": self.__tts_printed,
            "first_cells": self.__first_cells,
            "stages": self.stages,
        }

    def __reset_tts(self):
        self.__tts_matrix = None
        self.__tts_annotation = None
        self.__tts_words = None
        self.__tts_printed = None
        self.__first_cells = None

    def __install(self, matrix):
        if matrix is None:
            return None

        self.__reset_tts()
        annotated_matrix = annotate(matrix)
        words = identify_words(annotated_matrix)
        first_cells = get_first_cells(annotated_matrix)
        printed_html = print_crosswords(annotated_matrix, first_cells)

        self.__tts_matrix = matrix
        self.__tts_annotation = annotated_matrix
        self.__tts_words = words
        self.__first_cells = first_cells
        self.__tts_printed = printed_html

    def get(self, key):
        if key in self.__details.keys():
            return self.__details[key]
        if key == "all":
            return self.__details
        return None

    def get_all(self):
        return self.__details

    def set(self, words: str):
        if isinstance(words, str):
            self.__input_words = words
            words = [x.strip().upper() for x in words.split(",") if x.strip() != ""]
        elif isinstance(words, list):
            str_words = ",".join(words)
            self.__input_words = str_words
            words = [x.strip().upper() for x in words if x.strip() != ""]

        self._set_words(words)

    def create(self, strict=True):
        matrix = self._create_tts(separator=self.__separator)
        if strict:
            if matrix is None:
                return None
            else:
                self.__install(matrix)
        else:
            matrix = self.best_matrix
            self.__install(matrix)

    def recreate(self):
        matrix = self._create_tts(separator=self.__separator)
        self.__install(matrix)
