import time


def stage_decorator(timer=0.5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            on_success = kwargs.pop("on_success", None)
            on_error = kwargs.pop("on_error", None)
            is_true, messages = func(*args, **kwargs)
            time.sleep(timer)
            if is_true:
                if on_success:
                    on_success(messages)
            else:
                if on_error:
                    on_error(messages)

        return wrapper

    return decorator


@stage_decorator()
def word_processing(sessions):
    tts = sessions.get("tts")
    input_words = sessions.get("input_words")
    input_words_list = [x.strip() for x in input_words.split(",") if x.strip() != ""]
    tts.set(input_words_list)
    tts_words = tts.input_words
    if len(tts_words) > 0:
        sessions.update("input_words_list", tts)
        return True, "Berhasil menganalisis input kata-kata."
    else:
        return False, "Gagal menganalisis input kata-kata."


@stage_decorator()
def creating_matrix(sessions):
    tts = sessions.get("tts")
    tts.create_matrix()
    matrix = tts.matrix
    if matrix:
        sessions.update("tts_matrix", matrix)
        return True, "Berhasil membuat matriks TTS."
    else:
        return False, "Gagal membuat matriks TTS."


@stage_decorator()
def creating_annotation(sessions):
    tts = sessions.get("tts")
    annotation = tts.annotation()
    if annotation:
        sessions.update("tts_words", annotation)
        return True, "Berhasil membuat anotasi TTS."
    else:
        return False, "Gagal membuat anotasi TTS."


@stage_decorator()
def creating_printed_html(sessions):
    tts = sessions.get("tts")
    printed_html = tts.print()
    sessions.update("tts_printed", printed_html)
    return True, "Berhasil membuat TTS."
