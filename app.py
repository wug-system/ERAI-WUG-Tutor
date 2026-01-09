%%writefile app.py
import streamlit as st
from groq import Groq

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="ERAI - WUG Tutor", page_icon="🎓")

# Masukkan API Key Groq kamu di sini
# (Saran: Nanti kalau sudah dideploy, gunakan st.secrets untuk keamanan WUG)
GROQ_API_KEY = st.secrets["Ggsk_SapATkFzEnkbkuGflywsWGdyb3FY2Zw96bL9bOKY0wkoFoXo8ktJ"]

client = Groq(api_key=GROQ_API_KEY)

# --- STYLE VISUAL (WUG Standard) ---
st.title("🤖 ERAI")
st.caption("WUG Secure System Standard | Tutor Sebaya Interaktif")
st.divider()

# --- LOGIKA MEMORI CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat chat agar ERAI "ingat" percakapan sebelumnya
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT USER ---
if prompt := st.chat_input("Tanya apa hari ini?"):
    # Simpan pesan user ke memori
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon ERAI
    with st.chat_message("assistant"):
        # Instruksi Kepribadian ERAI
        system_prompt = (
            "Nama kamu ERAI. Kamu tutor sebaya standar WUG. "
            "Gaya bicara santai (aku-kamu), suportif, dan cerdas. "
            "DILARANG memberi jawaban langsung. Berikan bimbingan bertahap."
        )
        
        # Panggil API Groq
        full_messages = [{"role": "system", "content": system_prompt}] + \
                        [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            temperature=0.7,
        )
        
        response = completion.choices[0].message.content
        st.markdown(response)
        
    # Simpan respon ERAI ke memori
    st.session_state.messages.append({"role": "assistant", "content": response})
