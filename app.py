import streamlit as st

import google.generativeai as genai
import os


# 1. Konfigurasi Halaman & UI

st.set_page_config(

    page_title="Nuansa AI - Islamic Assistant",

    page_icon="🌙"
,
    layout="centered"

)


# Judul Aplikasi

st.title("🌙 Nuansa AI"
)
st.caption("Asisten Islami Pintar untuk Menemani Produktivitas & Ibadah Harianmu")


# 2. Inisialisasi API Key (Aman untuk GitHub)

# Di lokal: Simpan di Streamlit secrets atau environment variable

# Di Streamlit Cloud: Masukkan ke bagian Advanced Settings -> Secrets

if "GEMINI_API_KEY" in st.secrets:

    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

elif os.environ.get("GEMINI_API_KEY"):

    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

else:

    st.error("API Key Gemini tidak ditemukan! Harap konfigurasi GEMINI_API_KEY di Secrets Streamlit Anda.")

    st.stop()


# 3. Fitur Tambahan: Widget Rekomendasi di Sidebar (Agent Feature)

with st.sidebar:

    st.header("⚙️ Fitur Agent")
    

    # Fitur interaktif untuk memicu ingatan/rekomendasi chat

    st.subheader("💡 Inspirasi Hari Ini"
)
    topik_pilihan = st.selectbox(

        "Pilih fokus ibadahmu hari ini:",

        ["Manajemen Waktu Islami", "Tips Konsistensi Shalat Tahajud", "Adab Menuntut Ilmu", "Sabar dalam Menghadapi Ujian"]

    )
    


# 4. Inisialisasi Memori Chat (Short-term Memory)

if "messages" not in st.session_state:

    st.session_state.messages = []


# 5. System Instruction (Mengatur Persona & Gaya Bahasa AI Agent)

SYSTEM_INSTRUCTION = """

Anda adalah 'Nuansa AI', seorang Asisten Islami Pintar dan AI Agent yang bertindak sebagai teman diskusi yang bijak, hangat, dan santun.

- Gaya Bahasa: Gunakan bahasa Indonesia yang santai, bersahabat, namun tetap menghormati dan santun (Gunakan sapaan seperti 'Sobat Nuansa', 'Kamu', atau 'Kita'). Jangan terlalu kaku seperti robot, tapi tetap jaga adab.

- Domain Pengetahuan: Fokus pada edukasi Islami, produktivitas berbasis nilai Islam, motivasi ibadah, sejarah Islam, dan adab harian.

- Guardrails (Batasan): Jika ditanya soal fatwa hukum fikih yang sangat spesifik dan sensitif, berikan penjelasan umum yang menyejukkan, lalu sarankan dengan lembut untuk berkonsultasi kepada ulama atau kiai setempat demi kehati-hatian. Jangan menghakimi pengguna.

- Selalu sisipkan kutipan nilai kebaikan atau motivasi di akhir jawaban jika relevan.
"""


# Fungsi untuk memanggil model Gemini dengan System Instruction dan Chat History

def dapatkan_respon_gemini(messages_history):

    # Mengubah format riwayat pesan Streamlit ke format yang dipahami Gemini

    contents = []

    for msg in messages_history:

        role = "user" if msg["role"] == "user" else "model"

        contents.append({"role": role, "parts": [msg["content"]]})
        

    # Inisialisasi model dengan instruksi sistem

    model = genai.GenerativeModel(

        model_name="gemini-1.5-flash",

        system_instruction=SYSTEM_INSTRUCTION

    )
    

    try:

        response = model.generate_content(contents)

        return response.text

    except Exception as e:

        return f"Maaf ya, ada sedikit kendala teknis saat memproses pesan: {str(e)}"


# 6. Alur Logika Trigger dari Sidebar

if st.button("Bahas Topik Ini"):

    prompt_otomatis = f"Bisa berikan saya tips dan panduan praktis mengenai {topik_pilihan}?"

    st.session_state.messages.append({"role": "user", "content": prompt_otomatis})
    

    # Jalankan model langsung

    with st.spinner("Nuansa sedang merangkai kata..."):

        response_text = dapatkan_respon_gemini(st.session_state.messages)

        st.session_state.messages.append({"role": "assistant", "content": response_text})


# 7. Menampilkan Riwayat Obrolan dari Memori

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# 8. Input Chat dari Pengguna

if user_input := st.chat_input("Tanyakan sesuatu pada Nuansa... (misal: Tips tetap istiqomah?)"):

    # Tampilkan pesan pengguna di UI dan simpan ke memori

    with st.chat_message("user"):

        st.markdown(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})
    

    # Dapatkan respon dari AI Agent

    with st.chat_message("assistant"):

        with st.spinner("Nuansa sedang mengetik..."):

            response_text = dapatkan_respon_gemini(st.session_state.messages)

            st.markdown(response_text)
            

    # Simpan respon asisten ke memori

    st.session_state.messages.append({"role": "assistant", "content": response_text})