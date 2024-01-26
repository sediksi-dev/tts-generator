import streamlit as st
from helper.sessions import Sessions, PageSessions
import time

st.set_page_config(
    page_title="Buat TTS",
    page_icon=":books:",
    layout="centered",
    initial_sidebar_state="collapsed",
)


sessions = Sessions()
tts = sessions.get("tts_details")
uid = sessions.get("user_id")
page = PageSessions({"mode": "1-clue"})


def change_mode():
    if page.get("mode") == "1-clue":
        page.update("mode", "m-clue")
    else:
        page.update("mode", "1-clue")


st.title("SedikSilang - UBAH TTS")
st.markdown(
    """
Berhasil membuat TTS! Anda dapat melihat hasilnya di bawah ini.
Untuk mempublikasikan TTS ini, Anda dapat menyalin URL di bawah ini dan membagikannya kepada teman-teman Anda.
    """
)


expander = st.expander("Lihat TTS", expanded=True)
expander.write(f"{tts['printed']}<br>", unsafe_allow_html=True)
if expander.button("Ganti TTS", help="Ganti TTS Anda.", use_container_width=True):
    st.switch_page("pages/2_TTS_(UBAH).py")

sf = st.container(border=True)
# Judul TTS
sf.text_input(
    label="Judul TTS",
    value=sessions.get("tts_info")["title"],
    key="sf_title",
    autocomplete="off",
    placeholder="Judul TTS. Contoh: TTS SedikSilang",
)

# Penulis TTS
sf.text_input(
    label="Penulis TTS",
    value=sessions.get("tts_info")["author"],
    key="sf_author",
    autocomplete="full-name",
    placeholder="Nama Anda. Contoh: John Doe",
)

# Email Penulis TTS
sf.text_input(
    label="Email Penulis TTS",
    value=sessions.get("tts_info")["author"],
    key="sf_author_email",
    autocomplete="email",
    placeholder="Email Anda. Contoh: johndoe@gmail.com",
)

# Pilih, antara menambahkan clue pada masing-masing kata, atau memberikan satu clue untuk seluruh kata dalam TTS.
sf.radio(
    label="Jenis Clue",
    options=["Seluruh kata", "Masing-masing kata"],
    index=0,
    key="sf_clue_type",
    help="Pilih jenis clue yang ingin Anda tambahkan.",
    on_change=change_mode,
)

# Deskripsi TTS
if page.get("mode") == "1-clue":
    sf.text_area(
        label="Deskripsi TTS",
        value=sessions.get("tts_info")["description"],
        key="sf_description",
        help="Deskripsikan TTS Anda. Contoh: TTS ini dibuat untuk menguji pengetahuan umum.",
        max_chars=500,
        height=150,
        placeholder="Deskripsikan TTS Anda. Contoh: TTS ini dibuat untuk menguji pengetahuan umum.",
    )

    # Pilih 1 kata untuk ditampilkan pada tts
    sf.selectbox(
        label="Kata yang ingin ditampilkan",
        options=[word["word"] for word in tts["words"]],
        index=0,
        key="sf_selected_word",
        help="Pilih kata yang ingin ditampilkan pada TTS.",
    )
else:
    for word in tts["words"]:
        sf.text_input(
            label=f"Clue untuk kata {word['word']}",
            value="",
            key=f"sf_description_{word['word']}",
            help=f"Clue untuk kata {word['word']}.",
            placeholder=f"Clue untuk kata {word['word']}.",
        )


# Tombol Simpan
if sf.button(
    "Simpan TTS",
    help="Simpan TTS Anda ke dalam database kami.",
    type="primary",
    use_container_width=True,
):
    time.sleep(3)
    st.success("TTS berhasil disimpan!")
    st.balloons()
