import streamlit as st

st.set_page_config(
    page_title="Teka-Teki Silang Generator",
    page_icon=":100:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("Sediksilang")
st.subheader("Tantangan Teka Teki Silang Interaktif!")
st.markdown(
    """
Bergabunglah dalam petualangan kata di dunia digital, di mana kecepatan, kecerdasan, dan keakraban dengan kata-kata akan membawa Anda ke puncak _leaderboard_.
    """
)

st.markdown("## Apa itu Sediksilang?")
st.markdown(
    """
Sediksilang adalah platform inovatif yang menggabungkan kesenangan tradisional Teka Teki Silang dengan tantangan interaktif yang seru. Ciptakan, sebarkan, dan tantang teman-teman Anda dalam perlombaan kata-kata!
"""
)

st.markdown("## Fitur Unggulan")
st.markdown(
    """
- **Buat TTS Anda Sendiri:** Dengan beberapa klik saja, transformasikan kumpulan kata favorit Anda menjadi Teka Teki Silang yang menantang.
- **Bagikan dan Tantang:** Sebarkan TTS yang Anda buat melalui link unik. Tantang teman atau keluarga Anda untuk menyelesaikannya dalam waktu tercepat.
- **Satu Kesempatan, Satu Kemenangan:** Setiap teka-teki hanya bisa dijawab sekali. Siapkan strategi terbaik Anda!
- **Leaderboard:** Catat nama Anda di papan peringkat dan tunjukkan keahlian Anda dalam merangkai dan memecahkan kata-kata.
"""
)

st.markdown("## Cara Bermain")
st.markdown(
    """
1. **BUAT:** Masukkan kata-kata pilihan Anda dan biarkan Sediksilang mengubahnya menjadi TTS.
2. **BAGIKAN:** Dapatkan link unik dan ajak orang lain untuk bermain.
3. **MAINKAN:** Isi TTS dan berlombalah untuk mendapatkan waktu tercepat.
    """
)

with st.container():
    st.divider()
    st.markdown("## Siap menjadi master kata?")
    st.markdown(
        """
Klik tombol di bawah untuk membuat TTS Anda sendiri dan mulai bermain!
    """
    )
    if st.button("BUAT TTS SEKARANG", use_container_width=True, type="primary"):
        st.switch_page("pages/1_TTS_(BUAT).py")
    st.divider()
