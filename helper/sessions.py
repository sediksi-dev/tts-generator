import streamlit as st
from config import default_states as ds


class Sessions:
    def __init__(self, default_values: dict = ds.default_states):
        self.default_values = default_values

    # Inisialisasi session state
    def init(self):
        for key, value in self.default_values.items():
            if key not in st.session_state:
                st.session_state[key] = value

    # Ambil session state berdasarkan key
    def get(self, key):
        if key in st.session_state:
            return st.session_state[key]
        else:
            return None

    # Ambil semua session state
    def get_all(self):
        return st.session_state

    # Update session state
    def update(self, key, value):
        st.session_state[key] = value

    # Reset specific session state
    def reset(self, key):
        st.session_state[key] = self.default_values[key]

    # Reset all session state
    def reset_all(self, exclude: list = []):
        for key, value in self.default_values.items():
            if key not in exclude:
                st.session_state[key] = value


class PageSessions:
    def __init__(self, page_states: dict = {}):
        self.page_states = page_states
        self.__add_page_state()

    def __add_page_state(self):
        if "page_level" not in st.session_state:
            st.session_state["page_level"] = {}
        else:
            self.update("page_level", {})
        for key, value in self.page_states.items():
            if key not in st.session_state["page_level"]:
                st.session_state["page_level"][key] = value

    # Ambil session state berdasarkan key
    def get(self, key):
        if key in st.session_state["page_level"]:
            return st.session_state["page_level"][key]
        else:
            return None

    # Ambil semua session state
    def get_all(self):
        return st.session_state["page_level"]

    # Update session state
    def update(self, key, value):
        st.session_state["page_level"][key] = value

    # Reset specific session state
    def reset(self, key):
        st.session_state["page_level"][key] = self.page_states[key]

    # Reset all session state
    def reset_all(self, exclude: list = []):
        for key, value in self.page_states.items():
            if key not in exclude:
                st.session_state["page_level"][key] = value
