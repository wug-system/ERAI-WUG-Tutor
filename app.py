import streamlit as st
from groq import Groq

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="ERAI - WUG Tutor", page_icon="🎓")

# PANGGIL KUNCI DARI RAHASIA (Gunakan label saja)
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# --- STYLE VISUAL ---
st.title("🤖 ERAI")
st.caption("WUG Secure System Standard | Tutor Sebaya Personal")
st.divider()

# --- INISIALISASI MEMORI ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# --- TAHAP PERKENALAN ---
if not st.session_state.user_name:
    with st.chat_message("assistant"):
        st.markdown("Halo! Aku **ERAI**, tutor sebaya kamu. Sebelum kita mulai belajar, aku boleh tau nama panggilan kamu siapa?")
    
    if name_input := st.chat_input("Masukkan nama kamu..."):
        st.session_state.user_name = name_input
        st.session_state.messages.append({"role": "assistant", "content": f"Salam kenal, {name_input}! Senang banget bisa bantu kamu belajar hari ini. Ada materi yang mau kita bahas bareng?"})
        st.rerun()
else:
    # Tampilkan riwayat chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- LOGIKA CHAT UTAMA ---
    if prompt := st.chat_input(f"Tanya apa hari ini, {st.session_state.user_name}?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Update Instruksi ERAI: Lebih ngebantu, nggak pelit jawaban
            system_prompt = (
                f"Nama kamu ERAI. Kamu tutor sebaya standar WUG yang asik buat {st.session_state.user_name}. "
                f"Gaya bicara santai (aku-kamu). "
                f"Tugasmu: JANGAN cuma suruh siswa cari sendiri. "
                f"1. Berikan penjelasan konsep atau langkah-langkahnya dulu secara jelas. "
                f"2. Kasih contoh gampang atau analogi. "
                f"3. Baru di akhir ajak {st.session_state.user_name} buat nyelesaiin langkah terakhirnya."
            )
            
            full_messages = [{"role": "system", "content": system_prompt}] + \
                            [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=full_messages,
                temperature=0.8,
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
