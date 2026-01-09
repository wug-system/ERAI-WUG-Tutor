import streamlit as st
from groq import Groq
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="ERAI - WUG Tutor", page_icon="🎓")

# PANGGIL KUNCI DARI RAHASIA
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("API Key 'GROQ_API_KEY' tidak ditemukan di Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- STYLE VISUAL ---
st.title("🤖 ERAI")
st.caption("WUG Secure System Standard | Tutor Sebaya Interaktif")
st.divider()

# --- FUNGSI RENDER MATEMATIKA ---
# Fungsi ini memastikan simbol LaTeX render dengan sempurna di Streamlit
def render_math_content(text):
    # Mengubah format \[ ... \] atau \( ... \) menjadi format $ ... $ yang disukai Streamlit
    clean_text = text.replace(r"\[", "$$").replace(r"\]", "$$")
    clean_text = clean_text.replace(r"\(", "$").replace(r"\)", "$")
    return clean_text

# --- INISIALISASI MEMORI ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# --- TAHAP PERKENALAN ---
if not st.session_state.user_name:
    with st.chat_message("assistant"):
        st.markdown("Halo! Aku **ERAI**, tutor sebaya kamu. Sebelum kita mulai, nama panggilan kamu siapa?")
    
    if name_input := st.chat_input("Masukkan nama kamu..."):
        st.session_state.user_name = name_input
        st.session_state.messages.append({"role": "assistant", "content": f"Salam kenal, {name_input}! Mau bahas materi apa kita hari ini?"})
        st.rerun()
else:
    # Tampilkan riwayat chat dengan render matematika
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(render_math_content(message["content"]))

    # --- LOGIKA CHAT UTAMA ---
    if prompt := st.chat_input(f"Tanya apa hari ini, {st.session_state.user_name}?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(render_math_content(prompt))

        with st.chat_message("assistant"):
            # Update Instruksi ERAI: Paksa pakai format $...$
            system_prompt = (
                f"Nama kamu ERAI. Kamu tutor sebaya standar WUG untuk {st.session_state.user_name}. "
                "Gunakan bahasa santai (aku-kamu). "
                "WAJIB: Gunakan simbol '$' untuk semua rumus matematika. "
                "Contoh: tulis $x^2$ bukan x^2. Tulis $\\frac{a}{b}$ untuk pecahan. "
                "Jangan hanya kasih jawaban, jelaskan langkahnya secara asik."
            )
            
            full_messages = [{"role": "system", "content": system_prompt}] + \
                            [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=full_messages,
                    temperature=0.7,
                )
                
                response = completion.choices[0].message.content
                # Render langsung saat membalas
                st.markdown(render_math_content(response))
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
