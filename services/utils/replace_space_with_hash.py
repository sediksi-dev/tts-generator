def replace_space_with_hash(matrix):
    """
    Mengganti spasi dalam matriks dengan tanda hash (#).
    :param matrix: Matriks yang akan diubah.
    :return: Matriks dengan spasi diganti oleh tanda hash (#).
    """
    copied_matrix = [row for row in matrix]
    return [["#" if cell == " " else cell for cell in row] for row in copied_matrix]
