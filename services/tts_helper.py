import itertools
import time


class TTS_Helper:
    def __init__(self):
        self._stages = []  # Daftar tahapan yang telah dilalui
        self._counter = {}
        self.__iteration = {}
        self.__time = {
            "start": None,
            "end": None,
        }

    @property
    def iterator(self):
        return self.__iteration

    @property
    def stages(self):
        return self._stages

    @property
    def current_stage(self):
        return self.__get_current_stage()

    @property
    def counter(self):
        return self._counter

    @property
    def start_time(self):
        return self._time["start"]

    @property
    def end_time(self):
        return self._time["end"]

    @property
    def duration(self):
        return self.__get_duration()

    def __get_current_stage(self):
        return self.stages[-1] if len(self.stages) > 0 else None

    def __get_duration(self):
        if self.__time["end"] is None:
            return time.time() - self.__time["start"]
        return self.__time["end"] - self.__time["start"]

    def __add_stage(self, msg: str, state=None, **kwargs):
        if state == "warning":
            icon = "🟡"
        elif state == "success":
            icon = "🟢"
        elif state == "error":
            icon = "🔴"
        else:
            icon = "🔵"

        self.stages.append(
            {"message": f"{icon} {msg}", "timestamp": time.time()}, **kwargs
        )

    def __counting(self, key: str):
        if key not in self._counter.keys():
            self._counter[key] = 0
        self._counter[key] += 1

    def _logging(self, msg: str, state=None, key: str = None):
        if key is not None:
            self.__counting(key)
            msg = f"{msg} ({self._get_counter(key)})"
        self.__add_stage(msg, state)

    def _str_to_list(self, input_words):
        if isinstance(input_words, list):
            return [x.strip().upper() for x in input_words if x.strip() != ""]
        elif isinstance(input_words, str):
            return [
                x.strip().upper() for x in input_words.split(",") if x.strip() != ""
            ]
        return []

    def _set_start(self):
        self.__time["start"] = time.time()

    def _set_end(self):
        self.__time["end"] = time.time()

    def _get_counter(self, key: str):
        if key not in self._counter.keys():
            self._counter[key] = 0
        return self._counter[key]

    def _reset_counter(self, key: str):
        if key not in self.__iteration.keys():
            self.__iteration[key] = 0
        self.__iteration[key] += self._get_counter(key)
        self._counter[key] = 0

    def _reset_all_counter(self):
        for key in self._counter.keys():
            if key not in self.__iteration.keys():
                self.__iteration[key] = 0
            self.__iteration[key] += self._get_counter(key)
            self._reset_counter(key)

    def _get_all_combinations(self, words):
        # print(words)
        # Jika lebih dari 5 kata, maka buat chunk kata-kata berukuran 5
        if len(words) > 5:
            chunk_size = 3
            chunks = [
                words[i : i + chunk_size] for i in range(0, len(words), chunk_size)
            ]
            combinations = []
            for chunk in chunks:
                combinations.extend(list(itertools.permutations(chunk)))
            return combinations

        combinations = list(itertools.permutations(words))
        return combinations
