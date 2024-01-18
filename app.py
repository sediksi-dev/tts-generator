import streamlit as st
from generator.tts_generator import TTS

st.title("Teka-Teki Silang Generator")
st.markdown(
    """
    Teka-Teki Silang Generator adalah aplikasi web untuk membuat teka-teki silang.
    Aplikasi ini dibuat menggunakan Python dan Streamlit.
    Untuk membuat teka-teki silang, silahkan masukkan kata-kata yang ingin Anda gunakan.
    Kata-kata dipisahkan dengan koma.
    """
)

# Inisialisasi session state untuk berbagai variabel yang akan digunakan
# Ini akan memungkinkan informasi untuk dipertahankan selama sesi aplikasi
# Inisialisasi variabel session state jika belum ada
if "tts" not in st.session_state:
    st.session_state["tts"] = None

if "input_kata" not in st.session_state:
    st.session_state["input_kata"] = ""

if "tts_matrix" not in st.session_state:
    st.session_state["tts_matrix"] = None

if "tts_words" not in st.session_state:
    st.session_state["tts_words"] = None

if "tts_clues" not in st.session_state:
    st.session_state["tts_clues"] = {}

if "tts_button_text" not in st.session_state:
    st.session_state["tts_button_text"] = "BUAT"

if "display_clues_button" not in st.session_state:
    st.session_state["display_clues_button"] = False

if "display_clues_form" not in st.session_state:
    st.session_state["display_clues_form"] = False


# Fungsi yang mengembalikan format string dari detail kata untuk output
def output(wd):
    return f"- [{str(wd['group'])}] {wd['word']} ({len(wd['cells'])} kotak)\n"


# Fungsi untuk memvalidasi input kata dari pengguna
# Memisahkan kata berdasarkan koma dan membuang spasi yang tidak diperlukan
def daftar_kata(input_kata):
    validasi = input_kata.replace(" ", "").split(",")
    if len(validasi) == 1 and validasi[0] == "":
        return []
    else:
        return [kata for kata in validasi if kata.strip()]


# Inisialisasi TTS
@st.cache_data
def init_tts(daftar_kata):
    tts = TTS(daftar_kata)
    return tts


# Membuat matriks TTS dari input kata
def create_tts_matrix(tts):
    tts_matrix = tts.buat()
    return tts_matrix


# Mengembalikan session state ke nilai awal
def reset_input_kata():
    st.session_state["tts_matrix"] = None
    st.session_state["tts"] = None
    st.session_state["tts_button_text"] = "BUAT"
    st.session_state["input_kata"] = ""
    st.session_state["tts_clues"] = []
    st.session_state["tts_words"] = None
    st.session_state["display_clues_button"] = False
    st.session_state["display_clues_form"] = False


# Fungsi untuk menampilkan papan teka-teki silang yang telah dibuat
def display_tts(tts_matrix, tts, col=st):
    tts_html = tts.cetak(tts_matrix)
    col.markdown("### Papan TTS")
    col.write(tts_html, unsafe_allow_html=True)


# Menampilkan detil kata dalam papan TTS
def display_details(details):
    st.markdown("### Detil Kata")

    mendatar = [d for d in details if d["to"] == "mendatar"]
    menurun = [d for d in details if d["to"] == "menurun"]

    tab1, tab2 = st.columns(2)
    with tab1:
        st.markdown("##### Mendatar")
        st.write("\n".join([output(d) for d in mendatar]))

    with tab2:
        st.markdown("##### Menurun")
        st.write("\n".join([output(d) for d in menurun]))


# Fungsi untuk membuat form input dan tombol dalam aplikasi Streamlit
tts_form = st.form("tts_form")
input_kata = tts_form.text_input(
    "Masukkan kata-kata, pisahkan dengan koma",
    placeholder="Masukkan kata-kata, pisahkan dengan koma",
    value=st.session_state["input_kata"],
    autocomplete="off",
    key="words_input_field",
)

# Logika yang dijalankan ketika tombol "BUAT" atau "RESET" ditekan
# Ini termasuk validasi input dan pembuatan papan teka-teki silang
generate_tts = tts_form.form_submit_button(
    st.session_state["tts_button_text"],
    use_container_width=True,
    type="primary",
)

reset_tts = tts_form.form_submit_button(
    "RESET", use_container_width=True, on_click=reset_input_kata
)

# Aksi yang dilakukan ketika tombol "BUAT" ditekan
if generate_tts:
    # jika input kata kosong, tampilkan pesan kesalahan
    input_kata_list = daftar_kata(input_kata)
    if len(input_kata_list) == 0:
        st.toast(
            "Masukkan kata-kata yang ingin Anda gunakan.",
            icon="⚠️",
        )
    # jika input kata tidak kosong, buat papan TTS
    else:
        st.session_state["tts"] = init_tts(daftar_kata(input_kata))
        st.session_state["tts_matrix"] = create_tts_matrix(st.session_state["tts"])
        if st.session_state["tts_matrix"] is not None:
            st.session_state["tts_button_text"] = "PERBARUI"
            anotasi = st.session_state["tts"].anotasi(st.session_state["tts_matrix"])
            details = st.session_state["tts"].cari_kata(anotasi)
            st.session_state["tts_words"] = details
        st.rerun()

if st.session_state["tts_matrix"]:
    st.success("Berhasil membuat papan TTS!")
    st.divider()
    display_tts(st.session_state["tts_matrix"], st.session_state["tts"])
    st.empty()
    st.divider()
    st.session_state["display_clues_button"] = True


# Fungsi-fungsi untuk mengupdate clues dan menampilkan form untuk mengedit clues
def update_state_clues(input_clues):
    updated_words = []
    for word in st.session_state["tts_words"]:
        group = word["group"]
        updated_word = word.copy()
        updated_word["clue"] = input_clues.get(group, "")
        updated_words.append(updated_word)
    return updated_words


# Fungsi untuk menghandle submit pada form clues
def submit_new_clues():
    input_clues = {}
    words_list = st.session_state["tts_words"]
    for word in words_list:
        clue_input = st.session_state[f"clue_{word['group']}"]
        input_clues[word["group"]] = clue_input
    st.session_state["tts_clues"] = input_clues
    updated_words = update_state_clues(input_clues)
    st.session_state["tts_words"] = updated_words


# Menampilkan papan TTS, detail kata, dan form clues jika diperlukan
def toggle_clues_form():
    st.session_state["display_clues_form"] = not st.session_state["display_clues_form"]


# if st.session_state["display_clues_button"]:
#     st.button("Tambah Petunjuk", use_container_width=True, on_click=toggle_clues_form)


# Fungsi untuk menampilkan form clues
def display_clues_form():
    words_list = st.session_state["tts_words"]
    words_list = sorted(words_list, key=lambda x: x["group"])
    clues_form = st.form("clues_form")
    with clues_form:
        for word in words_list:
            st.text_input(
                f"Petunjuk untuk {word['word']}",
                value=word.get("clue", ""),
                key=f"clue_{word['group']}",
            )
        submitted = st.form_submit_button(
            "SIMPAN PETUNJUK", use_container_width=True, type="primary"
        )

    if submitted:
        submit_new_clues()
        st.success("Petunjuk berhasil disimpan!")
        st.session_state["display_clues_button"] = False

    # Tampilkan petunjuk menurun dan mendatar menggunakan column
    st.markdown("### Petunjuk")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Mendatar")
        st.write(
            "\n".join(
                [
                    f"- [{word['group']}] {word['clue']} = {word['word']}"
                    for word in st.session_state["tts_words"]
                    if word["to"] == "mendatar"
                ]
            )
        )
    with col2:
        st.markdown("##### Menurun")
        st.write(
            "\n".join(
                [
                    f"- [{word['group']}] {word['clue']} = {word['word']}"
                    for word in st.session_state["tts_words"]
                    if word["to"] == "menurun"
                ]
            )
        )


# Panggil fungsi display_clues_form jika tombol "Tambah Petunjuk" ditekan
if st.session_state["display_clues_button"]:
    if st.button("Tambah Petunjuk", use_container_width=True):
        toggle_clues_form()

if st.session_state["display_clues_form"]:
    display_clues_form()

# Akhir dari file app.py
