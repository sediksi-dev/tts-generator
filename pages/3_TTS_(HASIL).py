import streamlit as st
from helper.sessions import Sessions, PageSessions
from helper.db import DB

url: str = st.secrets.supabase.url
key: str = st.secrets.supabase.key
db: DB = DB(url, key)

st.set_page_config(
    page_title="Buat TTS",
    page_icon=":books:",
    layout="centered",
    initial_sidebar_state="collapsed",
)


sessions = Sessions()
tts = sessions.get("tts_details")
uid = sessions.get("user_id")
page = PageSessions({"mode": "Seluruh kata"})


def change_mode():
    page.update("mode", sessions.get("sf_clue_type"))


def get_clues():
    clues = {}
    if page.get("mode") == "Seluruh kata":
        clues = {
            "mode": "one_clue",
            "values": sessions.get("sf_one_clue"),
            "selected": sessions.get("sf_selected_word"),
        }
    elif page.get("mode") == "Setiap kata":
        mode = "each_clue"
        word_clues = []
        for _, word in enumerate(tts["words"]):
            word_clues.append(
                {
                    "word": word["word"],
                    "clue": sessions.get(f"sf_clues_{word['word']}"),
                }
            )
        clues = {"mode": mode, "values": word_clues}
    else:
        clues = {"mode": "error", "values": []}
    return clues


def get_author():
    tts_info = sessions.get("tts_info")
    author = tts_info["author"] or sessions.get("sf_author")
    author_email = tts_info["author_email"] or sessions.get("sf_author_email")
    return {
        "full_name": author,
        "email": author_email,
    }


def get_tts_data(id: str = None):
    tts_info = sessions.get("tts_info")
    results = {
        "uuid": sessions.get("session_id"),
        "title": tts_info["title"] or sessions.get("sf_title"),
        "matrix": {
            "raw": [list(x) for x in tts["matrix"]],
            "annotated": tts["annotation"],
        },
        "words": list(tts["words"]),
        "clues": get_clues(),
        "numbering": tts["first_cells"],
    }
    if id:
        results["id"] = id
    return results


def save_form():
    form_data = {
        "title": sessions.get("sf_title"),
        "author": sessions.get("sf_author"),
        "author_email": sessions.get("sf_author_email"),
        "clues": get_clues(),
    }

    sessions.update("tts_info", form_data)
    return form_data


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
    value=sessions.get("tts_info")["author_email"],
    key="sf_author_email",
    autocomplete="email",
    placeholder="Email Anda. Contoh: johndoe@gmail.com",
)

# Pilih, antara menambahkan clue pada masing-masing kata, atau memberikan satu clue untuk seluruh kata dalam TTS.
sf.radio(
    label="Berikan clue pada",
    options=["Seluruh kata", "Setiap kata"],
    index=0,
    key="sf_clue_type",
    help="Pilih jenis clue yang ingin Anda tambahkan.",
    on_change=change_mode,
    horizontal=True,
)

# Deskripsi TTS
if page.get("mode") == "Seluruh kata":
    sf.text_area(
        label="Deskripsi TTS",
        value=sessions.get("tts_info")["clues"]["values"],
        key="sf_one_clue",
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
        help="Kata yang dipilih akan ditampilkan pada awal Pengguna mengisi TTS.",
    )
else:
    for idx, word in enumerate(tts["words"]):
        sf.text_input(
            label=f"{word['word']}",
            key=f"sf_clues_{word['word']}",
            help=f"Berikan **clue** untuk kata {word['word']}.",
            placeholder=f"{word['word']}. Contoh: {word['word']} adalah nama saya.",
        )

# Tombol Simpan
if sf.button(
    "Simpan TTS",
    help="Simpan TTS Anda ke dalam database kami.",
    type="primary",
    use_container_width=True,
    on_click=save_form,
):
    author = get_author()
    tts_data = get_tts_data(uid)
    try:
        _submited, submited_tts = db.submit(author, tts_data)
        if _submited:
            st.success("TTS berhasil disimpan!")
            st.balloons()
            sessions.destroy()
            st.switch_page("Home.py")
        else:
            st.error(submited_tts)
    except Exception:
        st.error(submited_tts)
