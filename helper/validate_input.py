def validate_input(input_words):
    # Memisahkan kata-kata yang dipisahkan dengan koma
    input_words_list = [
        word.strip() for word in input_words.split(",") if word.strip() != ""
    ]

    # Jika input kata kosong, return error
    if input_words == "" or input_words is None:
        return False, "Input kata tidak boleh kosong."

    # Jika input kata hanya satu, return error
    if len(input_words_list) < 2:
        print(input_words_list)
        return False, "Input kata tidak boleh hanya satu."

    # Jika input kata lebih dari 10, return error
    if len(input_words_list) > 20:
        return False, "Input kata tidak boleh lebih dari 20 kata."

    # Jika input kata ada yang mengandung spasi, angka, atau simbol, return error
    for word in input_words_list:
        if " " in word:
            return False, "Input kata tidak boleh mengandung spasi."
        if any(char.isdigit() for char in word):
            return False, "Input kata tidak boleh mengandung angka."
        if not word.isalpha():
            return False, "Input kata tidak boleh mengandung simbol."

    # Jika input kata memiliki kata yang sama, return error
    if len(input_words_list) != len(set(input_words_list)):
        return False, "Input kata tidak boleh memiliki kata yang sama."

    # Jika input kata memiliki lebih dari 10 huruf, return error
    for word in input_words_list:
        if len(word) > 15:
            return False, "Input kata tidak boleh lebih dari 15 huruf."

    return True, ""
