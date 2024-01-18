def cetakPapanHTML(papan):
    jumlah_kolom = len(papan[0])
    jumlah_baris = len(papan)

    # wrapper_width = "50%" if not potrait else "20%"
    wrapper_width = f"{(40 * jumlah_kolom)}px"
    mobile_width = f"calc((100vw - 20px) / {(jumlah_kolom + 2)}))"
    mobile_font_size = f"calc(25vw / {(jumlah_baris + jumlah_kolom) / 2})"
    html = f"""
    <style>
        .tts-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: {wrapper_width};
            margin: 0 auto;
            max-width: 100%;
        }}
        .tts-container {{
            display: grid;
            grid-template-columns: repeat({jumlah_kolom}, 1fr);
            grid-gap: 0;
            width: 100%;
            padding: 10px;
            box-sizing: border-box;
        }}
        .tts-cell {{
            display: flex;
            justify-content: center;
            align-items: center;
            aspect-ratio: 1 / 1;  /* Menjaga sel menjadi kotak */
            background-color: #f0f0f0;
            border: 1px solid black;
            text-transform: uppercase;
            color: black;
            font-size: 16px
        }}
        .tts-cell-empty {{
            background-color: transparent;
            border: none;
        }}

        @media screen and (max-width: 600px) {{
            .tts-wrapper {{
                width: {mobile_width};
                padding: 2%;
            }}
            .tts-container {{
                padding: 5px;
            }}
            .tts-cell {{
                font-size: {mobile_font_size};
            }}
        }}
    </style>
    <div class='tts-wrapper'>
    <div class='tts-container'>
    """

    for baris in papan:
        for cell in baris:
            class_name = "tts-cell" if cell != " " else "tts-cell tts-cell-empty"
            html += f"<div class='{class_name}'>{cell if cell != ' ' else ''}</div>"

    html += "</div></div>"
    return html
