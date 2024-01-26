def print_crosswords(annotated_matrix, fcell):
    """
    Menghasilkan HTML dan CSS untuk menampilkan teka-teki silang.
    :param matrix: Matriks teka-teki silang.
    :param fcell: Koordinat sel pertama dari setiap kata.
    :return: String HTML yang merepresentasikan teka-teki silang.
    """
    matrix = [[cell["value"] for cell in row] for row in annotated_matrix]
    fcell_keys = fcell.keys()

    num_columns = len(matrix[0])
    num_rows = len(matrix)

    # Mengatur lebar wrapper
    wrapper_width = f"{40 * num_columns}px"
    mobile_width = "calc(100vw - 20px)"

    ratio = (num_rows + num_columns) / 2
    font_size = f"calc(40vw / {ratio})" if ratio > 30 else "16px"
    font_size_counter = f"calc(20vw / {ratio})" if ratio > 30 else "12px"

    mobile_font_size = f"calc(50vw / {ratio})" if ratio > 30 else "14px"
    mobile_font_size_counter = f"calc(25vw / {ratio })" if ratio > 30 else "10px"

    def add_counter(number):
        return f"<span class='counter'>{number}</span>"

    # Membuat HTML dan CSS
    html = f"""
    <style>
        .cw-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto;
            width: 100%;
            background: white;
        }}
        .cw-container {{
            display: grid;
            grid-template-columns: repeat({num_columns}, 1fr);
            grid-gap: 0;
            width: {wrapper_width};
            padding: 10px;
            box-sizing: border-box;
        }}
        .cw-cell {{
            display: flex;
            justify-content: center;
            align-items: center;
            aspect-ratio: 1 / 1;  /* Memastikan sel berbentuk kotak */
            background-color: white;
            border: 1px solid black;
            text-transform: uppercase;
            color: black;
            font-size: {font_size};
            position: relative;
        }}
        .cw-cell-empty {{
            background-color: transparent;
            border: none;
        }}
        .counter {{
            position: absolute;
            top: 0;
            left: 0;
            font-size: {font_size_counter};
            line-height: 12px;
            color: #2f2f2f;
            padding: 2px;
            padding-left: 4px;
        }}
        @media screen and (max-width: 600px) {{
            .cw-wrapper {{
                width: {mobile_width};
                padding: 2%;
            }}
            .cw-container {{
                padding: 5px;
            }}
            .cw-cell {{
                font-size: {mobile_font_size};
            }}
            .counter {{
                font-size: {mobile_font_size_counter};
                line-height: {mobile_font_size_counter};
                padding: 1%;
            }}
        }}
    </style>
    <div class='cw-wrapper'>
    <div class='cw-container'>
    """

    # Membuat sel untuk setiap elemen dalam matriks
    for row in annotated_matrix:
        for cell in row:
            value = cell["value"]
            is_empty = cell["empty"]
            code = cell["code"]
            group = fcell[code] if code in fcell_keys else 0
            counter = add_counter(group) if code in fcell_keys else ""

            class_name = "cw-cell" if not is_empty else "cw-cell cw-cell-empty"
            class_name += f" group-{group}" if group != 0 else ""
            html += f"<div class='{class_name}'>{value if value != ' ' else ''} {counter}</div>"

    html += "</div></div>"
    return html
