def rotate(matrix):
    rotated_matrix = []
    for col in range(len(matrix[0])):
        rotated_matrix.append([])
        for row in range(len(matrix)):
            rotated_matrix[col].append(matrix[row][col])

    return rotated_matrix
