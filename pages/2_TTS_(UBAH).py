import streamlit as st
import time
from helper.sessions import Sessions, PageSessions
from services.core import TTS_Generator

st.set_page_config(
    page_title="Buat TTS",
    page_icon=":books:",
    layout="centered",
    initial_sidebar_state="collapsed",
)


sessions = Sessions()
if sessions.get("tts") is None:
    tts = TTS_Generator()
else:
    tts = sessions.get("tts")

page = PageSessions(
    {
        "status": "idle",  # idle, creating, created, error
    }
)


st.title("SedikSilang - UBAH TTS")
if st.button("< Ganti Kata-kata"):
    st.switch_page("pages/1_TTS_(BUAT).py")
st.markdown(
    """
Mulai dengan memasukkan kata-kata yang Anda buat ke dalam kolom di bawah ini. Pastikan untuk memisahkan setiap kata dengan tanda koma.
Setelah itu, klik tombol **Buat TTS** untuk melanjutkan.
    """
)

page_status = page.get("status")


def tts_created():
    page.update("status", "created")
    st.rerun()


def tts_error():
    page.update("status", "error")
    st.rerun()


def tts_creating():
    page.update("status", "creating")


def next_page():
    sessions.update("tts_details", tts.get_all())


input_words = sessions.get("input_words")
if tts.get("words") is None:
    tts.set(input_words)
    tts.create()
    result = tts.get("printed")
else:
    result = tts.get("printed")

tts_container = st.empty()

if page_status == "idle":
    tts_container.status("Sedang membuat TTS...")
    time.sleep(0.5)
    if result is not None:
        tts_created()
    else:
        tts_error()

col1, col2 = st.columns(2)

if page_status == "creating":
    tts_container.empty()
    tts_container.status("Sedang membuat TTS...")
    time.sleep(0.5)
    tts.recreate()
    result = tts.get("printed")
    if result is not None:
        tts_created()
    else:
        tts_error()

if page_status == "created":
    tts_container.write(f"{result}<br>", unsafe_allow_html=True)

if page_status == "error":
    tts_container.error("Gagal membuat TTS. Silakan coba lagi.")

if col2.button(
    "Selanjutnya",
    use_container_width=True,
    type="primary",
    disabled=page_status != "created",
    on_click=next_page,
):
    tts_container.empty()
    st.switch_page("pages/3_TTS_(HASIL).py")

col1.button(
    "Buat TTS Baru",
    use_container_width=True,
    type="secondary",
    on_click=tts_creating,
    disabled=page_status != "created",
)
