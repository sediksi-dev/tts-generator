from supabase import create_client, Client
import streamlit as st
from helper.sessions import Sessions

url: str = st.secrets.supabase.url
key: str = st.secrets.supabase.key
supabase: Client = create_client(url, key)


st.set_page_config(
    page_title="Buat TTS",
    page_icon=":books:",
    layout="centered",
    initial_sidebar_state="collapsed",
)


sessions = Sessions()
tts = sessions.get("tts_details")
uid = sessions.get("user_id")

data = {
    "uuid": uid,
    "author": sessions.get("tts_info")["author"],
    "author_email": sessions.get("tts_info")["author_email"],
    "title": sessions.get("tts_info")["title"],
    "matrix": {
        "raw": [list(x) for x in tts["matrix"]],
        "annotated": tts["annotation"],
    },
    "words": list(tts["words"]),
    "numbering": tts["first_cells"],
    "clues": sessions.get("tts_info")["clues"],
    "author_id": 1,
}

st.write(uid)


def check_author(email: str):
    try:
        author, count = (
            supabase.table("authors").select("*").eq("email", email).execute()
        )
        if count is None:
            st.write("Error: ", author)
            return False
        return author[1][0]
    except Exception:
        return False


def create_author(data: dict):
    try:
        author, count = supabase.table("authors").insert(data).execute()
        print(author, count)
        return author
    except Exception:
        return False


if st.button("Submit"):
    try:
        author = create_author(
            {"full_name": "Winda Noviati", "email": "windaisnaen@gmail.com"}
        )
        st.write(author)
    except Exception as e:
        st.write("Error: ", e)
        st.write("Data gagal diinput")
