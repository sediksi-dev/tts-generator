from .identify_words import identify_words


def get_first_cells(annotated_matrix):
    """
    Mencari sel pertama pada setiap kata pada TTS.
    :return: Dictionary yang berisi sel pertama dari setiap kata pada TTS.
    """
    fcells = {}
    group_counter = 1
    results = identify_words(annotated_matrix)
    for result in results:
        fcell = result["cells"][0]
        if fcell not in fcells:
            fcells[fcell] = group_counter
            group_counter += 1
        result["group"] = fcells[fcell]

    return fcells
