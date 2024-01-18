# Fungsi untuk mengganti nilai " " (spasi) pada array of array of string menjadi tanda "#"
def replace_space_with_hash(array):
    # Buat array baru untuk menyimpan hasil
    new_array = []
    # Looping untuk setiap sub-array dalam array
    for sub_array in array:
        # Buat sub-array baru untuk menyimpan hasil
        new_sub_array = []
        # Looping untuk setiap elemen dalam sub-array
        for element in sub_array:
            # Jika elemen adalah " ", ganti dengan "#"
            if element == " ":
                new_sub_array.append("#")
            # Jika tidak, biarkan elemen tetap sama
            else:
                new_sub_array.append(element)
        # Tambahkan sub-array baru ke array baru
        new_array.append(new_sub_array)
    # Kembalikan array baru
    return new_array
