import streamlit as st
import uuid
from helper.sessions import Sessions, PageSessions
from helper.validate_input import validate_input
from services.core import TTS_Generator

st.set_page_config(
    page_title="Buat TTS",
    page_icon=":pencil2:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

sessions = Sessions()
sessions.init()
sessions.update("session_id", str(uuid.uuid4()))
page = PageSessions({"stages": 0})

if sessions.get("tts") is None:
    tts = TTS_Generator()
else:
    tts = sessions.get("tts")

st.title("SedikSilang - Buat TTS")


st.markdown(
    """
Mulai dengan memasukkan kata-kata yang Anda buat ke dalam kolom di bawah ini. Pastikan untuk memisahkan setiap kata dengan tanda koma.
Setelah itu, klik tombol **Buat TTS** untuk melanjutkan.
    """
)

cf = st.form(key="create_tts")
cf.text_area(
    "Masukkan kata-kata yang ingin Anda masukkan ke dalam TTS",
    key="form_input_words",
    height=50,
    placeholder="Contoh: kata1, kata2, kata3, kata4",
    value=sessions.get("input_words"),
)
cf_notif = cf.empty()
cf_submit = cf.form_submit_button("Buat TTS", type="primary", use_container_width=True)

if cf_submit:
    form_input_words = sessions.get("form_input_words")
    is_valid, messages = validate_input(form_input_words)
    if not is_valid:
        cf_notif.error(messages)
    else:
        sessions.update("input_words", form_input_words)
        st.switch_page("pages/2_TTS_(UBAH).py")
