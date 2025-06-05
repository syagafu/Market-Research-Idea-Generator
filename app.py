import streamlit as st
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np

# --- API Key & Model ---
# Coba ambil dari secrets, jika tidak ada akan kosong
API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")

st.set_page_config(
    page_title="Market Research & Ideation Tool",
    layout="wide",
    page_icon="🛒"  # <-- INI FAVICON BARU
)
# Ganti logo roket dengan logo marketplace (misal: ikon keranjang belanja dari emoji)
st.markdown('''
    <style>
    @keyframes cart-move {
        0% { transform: translateX(0) scale(1) rotate(-2deg); }
        10% { transform: translateX(6px) scale(1.05) rotate(2deg); }
        20% { transform: translateX(12px) scale(1.08) rotate(-2deg); }
        30% { transform: translateX(8px) scale(1.04) rotate(2deg); }
        40% { transform: translateX(0) scale(1) rotate(-2deg); }
        50% { transform: translateX(-6px) scale(1.05) rotate(2deg); }
        60% { transform: translateX(-12px) scale(1.08) rotate(-2deg); }
        70% { transform: translateX(-8px) scale(1.04) rotate(2deg); }
        80% { transform: translateX(0) scale(1) rotate(-2deg); }
        100% { transform: translateX(0) scale(1) rotate(-2deg); }
    }
    .cart-anim {
        display: inline-block;
        animation: cart-move 2.5s infinite cubic-bezier(.4,1.6,.6,1);
        font-size: 2.5rem;
        vertical-align: middle;
    }
    </style>
    <h1 style="text-align:center;"><span class="cart-anim">🛒</span> Trend Market Research & Idea Generator</h1>
''', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:gray; font-size:1.2em;">Riset pasar, analisis ide, dan perbandingan strategi dengan AI!</p>', unsafe_allow_html=True)

# --- Sidebar - Pilihan Model AI ---
st.sidebar.header('Pengaturan Model AI')

# Input API Key
st.sidebar.subheader('API Key OpenRouter')
api_key_input = st.sidebar.text_input(
    "Masukkan API Key OpenRouter Anda", 
    value=API_KEY if API_KEY else "",
    type="password",
    help="Dapatkan API key gratis di https://openrouter.ai"
)

# Gunakan API key dari input jika ada, jika tidak gunakan dari secrets
FINAL_API_KEY = api_key_input if api_key_input.strip() else API_KEY

if not FINAL_API_KEY:
    st.sidebar.error("⚠️ API Key belum dimasukkan!")
    st.sidebar.markdown("""
    **Cara mendapatkan API Key:**
    1. Kunjungi [OpenRouter.ai](https://openrouter.ai)
    2. Daftar akun baru (gratis)
    3. Pergi ke bagian Keys/API
    4. Generate API key baru
    5. Masukkan di field di atas
    """)
else:
    st.sidebar.success("✅ API Key tersedia")

st.sidebar.markdown('---')

model_options = {
    'Deepseek Chat (Default)': 'deepseek/deepseek-chat-v3-0324',
    'Mistral Small': 'mistralai/devstral-small',
    'Mistral 7B': 'mistralai/mistral-7b-instruct'
}
selected_model_label = st.sidebar.selectbox('Pilih Model AI', list(model_options.keys()), index=0, key='model_ai_selectbox')
MODEL_NAME = model_options[selected_model_label]
st.sidebar.markdown('---')

# --- Sidebar BEP saja ---
st.sidebar.header('Simulasi Break Even Point (BEP)')
modal_bep = st.sidebar.number_input('Modal Awal (Rp)', min_value=0, value=0, step=1000000, format='%d', key='bep_modal', placeholder="Contoh: 10.000.000")
biaya_operasional_bep = st.sidebar.number_input('Biaya Operasional per Bulan (Rp)', min_value=0, value=0, step=500000, format='%d', key='bep_operasional', placeholder="Contoh: 2.000.000")
omzet_bep = st.sidebar.number_input('Omzet per Bulan (Rp)', min_value=0, value=0, step=500000, format='%d', key='bep_omzet', placeholder="Contoh: 5.000.000")

if st.sidebar.button('Hitung BEP'):
    if omzet_bep <= biaya_operasional_bep:
        st.sidebar.warning('Omzet per bulan harus lebih besar dari biaya operasional untuk bisa BEP!')
    else:
        bulan_bep = modal_bep / (omzet_bep - biaya_operasional_bep)
        bulan_bep_int = int(bulan_bep) if bulan_bep == int(bulan_bep) else int(bulan_bep) + 1
        st.sidebar.markdown(f"**Estimasi Break Even Point (BEP):**")
        st.sidebar.markdown(f"Anda akan balik modal dalam **{bulan_bep_int} bulan**.")
        st.sidebar.markdown(f"(Perhitungan: Modal / (Omzet - Biaya Operasional))")

# --- Fungsi OpenRouter ---
def call_openrouter(prompt, api_key, model_name):
    if not api_key.strip():
        st.error("❌ API Key tidak valid atau kosong!")
        return ""
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1200,  # Ditingkatkan agar output tidak terpotong
        "temperature": 0.7,
    }
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    try:
        response = requests.post(api_url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            hasil_json = response.json()
            if hasil_json.get("choices"):
                return hasil_json["choices"][0]["message"]["content"].strip()
            return "Tidak ada hasil."
        elif response.status_code == 401:
            st.error("❌ API Key tidak valid! Silakan periksa kembali API key Anda.")
            return ""
        elif response.status_code == 402:
            st.error("❌ Kredit/balance habis! Silakan top up balance di OpenRouter.ai")
            return ""
        elif response.status_code == 429:
            st.error("❌ Terlalu banyak request! Tunggu sebentar dan coba lagi.")
            return ""
        else:
            st.error(f"❌ Error dari server: {response.status_code} - {response.text}")
            return ""
    except Exception as e:
        st.error(f"❌ Error koneksi: {e}")
        return ""

# --- Prompt Generator ---
def buat_prompt_ide(segmen, pain_point, tren, kompetitor):
    return f"""Buatkan 3 ide produk/layanan baru untuk riset pasar berikut:
- Segmen pasar: {segmen}
- Masalah konsumen: {pain_point}
- Tren pasar: {tren}
- Kompetitor: {kompetitor}
Untuk setiap ide, berikan:
1. Deskripsi singkat ide
2. Analisis potensi target pasar
3. Saran strategi pemasaran awal
4. Potensi keunggulan kompetitif
5. Prediksi tantangan/riskonya
6. Poin-poin SWOT sederhana
Format: Ide 1:..., Ide 2:..., Ide 3:...
Pastikan SEMUA ide lengkap, tidak ada bagian yang terpotong, dan output selesai hingga Ide 3."""

def buat_prompt_perbandingan(ide_terpilih, kriteria):
    return f"""Bandingkan ide-ide berikut berdasarkan kriteria:
Kriteria: {', '.join(kriteria)}
Ide:
{chr(10).join([f'{i+1}. {ide}' for i, ide in enumerate(ide_terpilih)])}
Untuk setiap ide, beri skor (1-5) yang disajikan dalam format tabel, pastikan didalam tabel skor hanya ada format angka tanpa perlu penjelasan di tabel skor. lalu berikan Ringkasan Analisis dari poin-poin dibawah tabel."""

# --- UI dengan Multi Tab: Generator Ide & Perbandingan Hasil ---
st.markdown("""
    <style>
    /* Reset dan perbaiki tampilan tab agar tetap kontras di mode malam/terang, tanpa efek pop-up dan tanpa background gradasi kedua */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: stretch !important;
        background: var(--background-color, #fff) !important;
        border-radius: 18px 18px 0 0 !important;
        box-shadow: 0 2px 12px rgba(79,140,255,0.10);
        padding: 0.25rem 0.5rem 0 0.5rem;
        margin-bottom: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        text-align: center !important;
        font-size: 1.13em !important;
        font-weight: 600 !important;
        border-radius: 16px 16px 0 0 !important;
        margin: 0 8px 0 8px !important;
        transition: background 0.18s, color 0.18s, box-shadow 0.18s;
        background: var(--tab-bg, #f5faff) !important;
        color: var(--tab-fg, #222) !important;
        box-shadow: none !important;
        border: 1.5px solid transparent !important;
        border-bottom: none !important;
        outline: none !important;
        opacity: 0.92;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--tab-hover-bg, #e3e3e3) !important;
        color: var(--primary-color, #235390) !important;
        opacity: 1;
        cursor: pointer;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--tab-active-bg, #fff) !important;
        color: var(--primary-color, #235390) !important;
        box-shadow: 0 4px 18px rgba(79,140,255,0.13), 0 1.5px 8px rgba(0,0,0,0.04);
        border-bottom: 2.5px solid #4f8cff !important;
        z-index: 3;
        opacity: 1;
        border: 1.5px solid #4f8cff !important;
        border-bottom: none !important;
    }
    /* Dark mode overrides */
    @media (prefers-color-scheme: dark) {
        .stTabs [data-baseweb="tab-list"] {
            background: #18191a !important;
        }
        .stTabs [data-baseweb="tab"] {
            background: #23272f !important;
            color: #e0e0e0 !important;
            border: 1.5px solid #23272f !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background: #31343b !important;
            color: #4f8cff !important;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: #18191a !important;
            color: #4f8cff !important;
            border: 1.5px solid #4f8cff !important;
            box-shadow: 0 4px 18px rgba(79,140,255,0.18), 0 1.5px 8px rgba(0,0,0,0.10);
        }
    }
    </style>
""", unsafe_allow_html=True)
tabs = st.tabs(["Generator Ide", "Perbandingan Hasil", "Visualisasi Perbandingan Skor Ide"])

# Tab 1: Generator Ide
with tabs[0]:
    # --- Input Riset Pasar & Ide Produk (pindah dari sidebar ke tab 1) ---
    st.markdown('### Input Riset Pasar & Ide Produk')
    segmen = st.text_input("Segmen Pasar Target", placeholder="Mahasiswa urban, ibu rumah tangga", key="tab1_segmen")
    pain_point = st.text_input("Masalah Konsumen (Pain Point)", placeholder="Kost mahal, Sulit cari makanan sehat", key="tab1_pain_point")
    tren = st.text_input("Tren Pasar Saat Ini (Opsional)", placeholder="Produk berkelanjutan, layanan AI", key="tab1_tren")
    kompetitor = st.text_input("Nama/Jenis Kompetitor (Opsional)", placeholder="Teh Botol, Lemonilo, Netflix", key="tab1_kompetitor")
    st.markdown('---')
    st.markdown('### Kriteria Perbandingan (Opsional)')
    kriteria_default = ["Potensi Pasar", "Kesulitan Implementasi", "Inovasi", "Modal Awal"]
    kriteria_user = st.text_area("Kriteria Tambahan (pisahkan dengan koma)", placeholder="Contoh: Margin, Daya Tahan Produk", key="tab1_kriteria")
    if kriteria_user:
        kriteria_list = kriteria_default + [k.strip() for k in kriteria_user.split(",") if k.strip()]
    else:
        kriteria_list = kriteria_default
    st.markdown('---')
    # --- Generate Ide ---
    custom_btn_css = """
    <style>
    .custom-btn-gen button {
        background: linear-gradient(90deg, #4f8cff 0%, #235390 100%) !important;
        color: #fff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 1.1em !important;
        box-shadow: 0 2px 8px rgba(79,140,255,0.15);
        transition: background 0.2s;
    }
    .custom-btn-gen button:hover {
        background: linear-gradient(90deg, #235390 0%, #4f8cff 100%) !important;
        color: #fff !important;
        box-shadow: 0 4px 16px rgba(79,140,255,0.25);
    }
    </style>
    """
    st.markdown(custom_btn_css, unsafe_allow_html=True)
    # Custom CSS untuk SEMUA tombol Streamlit (bukan hanya .custom-btn-gen)
    custom_btn_css = """
    <style>
    button[kind="primary"], button[kind="secondary"], .stButton > button {
        background: linear-gradient(90deg, #4f8cff 0%, #235390 100%) !important;
        color: #fff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 1.1em !important;
        box-shadow: 0 2px 8px rgba(79,140,255,0.15);
        transition: background 0.2s, transform 0.15s, box-shadow 0.15s;
    }
    button[kind="primary"]:hover, button[kind="secondary"]:hover, .stButton > button:hover {
        background: linear-gradient(90deg, #235390 0%, #4f8cff 100%) !important;
        color: #fff !important;
        box-shadow: 0 8px 24px rgba(79,140,255,0.30);
        transform: scale(1.06);    }
    </style>
    """
    st.markdown(custom_btn_css, unsafe_allow_html=True)
    # Tooltip popup untuk tombol
    st.markdown('<div class="custom-btn-gen" title="Klik untuk menghasilkan ide dan analisis berdasarkan input Anda">', unsafe_allow_html=True)
    
    if st.button("🔍 Hasilkan Ide & Analisis", use_container_width=True):
        if not segmen or not pain_point:
            st.warning("Isi minimal segmen pasar dan masalah konsumen!")
        elif not FINAL_API_KEY:
            st.error("❌ Masukkan API Key OpenRouter terlebih dahulu di sidebar!")
        else:
            with st.spinner("Sedang riset dan menyusun ide..."):
                prompt = buat_prompt_ide(segmen, pain_point, tren, kompetitor)
                hasil = call_openrouter(prompt, FINAL_API_KEY, MODEL_NAME)
                # Jika gagal (hasil kosong), jangan tampilkan hasil & Tanya AI
                if not hasil.strip():
                    st.session_state['last_ide'] = []
                    st.session_state['hasil_ide_md'] = ''
                    st.session_state['just_generated'] = True
                else:
                    ide_list = [x.strip() for x in hasil.split('Ide ')[1:]] if 'Ide 1:' in hasil else []
                    ide_list = [ide for ide in ide_list if not ide.lower().startswith('semua ide telah lengkap') and not ide.lower().startswith('setiap ide mencakup')]
                    st.session_state['last_ide'] = ide_list
                    st.session_state['hasil_ide_md'] = hasil
                    st.session_state['just_generated'] = False  # Reset langsung setelah generate ide
                    if len(ide_list) < 3:
                        st.warning("⚠️ Hasil AI tampaknya terpotong. Coba klik tombol lagi, atau perpendek input/segmen/tren/kompetitor.")

    # Tampilkan hasil & Tanya AI hanya jika hasil_ide_md tidak kosong dan just_generated False
    if st.session_state.get('hasil_ide_md') and not st.session_state.get('just_generated'):
        st.subheader("Hasil Ide & Analisis:")
        st.markdown(st.session_state['hasil_ide_md'])
        st.session_state['just_generated'] = False
        # Tanya AI
        with st.expander("Personalisasi AI: Tanya AI", expanded=False):
            st.markdown("Tanyakan apa saja tentang ide yang dihasilkan di atas.")
            st.caption("""Contoh:
- Apa keunggulan ide 2 dibanding kompetitor?
- Bagaimana strategi pemasaran untuk ide 1?
- Berapa modal dan omset untuk ide 1?
- dll""")
            user_question = st.text_input("Pertanyaan untuk AI", key="tanya_ai_input")
            if st.button("Tanya AI", key="tanya_ai_btn"):
                if not user_question.strip():
                    st.warning("Masukkan pertanyaan terlebih dahulu.")
                else:
                    with st.spinner("Sedang memproses pertanyaan Anda..."):
                        context_ide = st.session_state['hasil_ide_md']
                        prompt_tanya = f"Berikut hasil ide dan analisis:\n{context_ide}\n\nJawab pertanyaan berikut secara spesifik dan ringkas, gunakan data dari ide di atas jika relevan.\nPertanyaan: {user_question}"
                        jawaban_ai = call_openrouter(prompt_tanya, FINAL_API_KEY, MODEL_NAME)
                        st.markdown(f"**Jawaban AI:**\n{jawaban_ai}")
        # Tambahkan tombol ganti model di tab 1
        st.markdown('---')
        st.markdown('<div class="custom-btn-gen" title="Ganti model AI untuk hasil ide yang berbeda">', unsafe_allow_html=True)
        if st.button('Apa anda ingin menggunakan model lain untuk generate ide?', key='btn_ganti_model_tab1', use_container_width=True):
            st.info('Silakan pilih model AI lain di sidebar pada bagian "Pengaturan Model AI", lalu klik tombol "🔍 Hasilkan Ide & Analisis" untuk generate ide baru.')
        st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Perbandingan Hasil
with tabs[1]:
    if 'last_ide' not in st.session_state or not st.session_state['last_ide']:
        st.info("Silakan generate ide terlebih dahulu di tab 'Generator Ide'.")
    else:
        st.subheader("Pilih Ide untuk Dibandingkan:")
        def get_ide_label(ide_text, idx):
            lines = ide_text.splitlines()
            for line in lines:
                if line.strip() and not line.strip().lower().startswith('deskripsi'):
                    return line.strip()[:60]
            return f"Ide {idx+1}"
        ide_labels = [get_ide_label(ide, i) for i, ide in enumerate(st.session_state['last_ide'])]
        label_to_ide = {get_ide_label(ide, i): ide for i, ide in enumerate(st.session_state['last_ide'])}
        selected_labels = st.multiselect("Pilih ide (minimal 2):", ide_labels, key="compare_ideas")
        selected = [label_to_ide[l] for l in selected_labels]
        if len(selected) >= 2:
            if st.button("⚖️ Bandingkan Ide", key="compare_btn", use_container_width=True):
                with st.spinner("Membandingkan ide dengan AI..."):
                    prompt_cmp = buat_prompt_perbandingan(selected, kriteria_list)
                    hasil_cmp = call_openrouter(prompt_cmp, FINAL_API_KEY, MODEL_NAME)
                    st.session_state['hasil_perbandingan'] = hasil_cmp
                    st.session_state['compare_selected'] = selected_labels
        if st.session_state.get('hasil_perbandingan'):
            st.subheader("Hasil Perbandingan:")
            lines = st.session_state['hasil_perbandingan'].splitlines()
            table_lines = []
            extra_lines = []
            penjelasan_idx = None
            for idx, l in enumerate(lines):
                if 'Penjelasan per Kriteria' in l:
                    penjelasan_idx = idx
                    break
                table_lines.append(l)
            if penjelasan_idx is not None:
                extra_lines = [l for l in lines[penjelasan_idx:] if not l.strip().startswith('ua ideua ide telah lengkap')]
            st.markdown('\n'.join(table_lines))
            if extra_lines:
                st.markdown('<div style="text-align:left; max-width:900px; margin: 0 auto;">' + '\n'.join(extra_lines) + '</div>', unsafe_allow_html=True)
            st.markdown('---')
            if st.button('Apa anda ingin menggunakan model lain untuk generate ide?', key='btn_ganti_model', use_container_width=True):
                st.info('Silakan pilih model AI lain di sidebar pada bagian "Pengaturan Model AI", lalu klik tombol "🔍 Hasilkan Ide & Analisis" yang ada di tab "Generator Ide" untuk generate ide baru.')

# Tab 3: Visualisasi Perbandingan Skor Ide
with tabs[2]:
    if not st.session_state.get('hasil_perbandingan'):
        st.info("Tab ini akan aktif setelah Anda melakukan perbandingan ide di tab 'Perbandingan Hasil'.")
    else:
        st.subheader("Bar Chart: Rata-rata Skor Kriteria per Ide")
        hasil_perbandingan = st.session_state['hasil_perbandingan']
        # --- Ekstrak tabel skor dari hasil perbandingan ---
        def extract_scores_from_table(text):
            lines = text.splitlines()
            table_lines = [l for l in lines if '|' in l and re.search(r'\d', l)]
            if not table_lines:
                return None, None
            header = [h.strip() for h in table_lines[0].split('|') if h.strip()]
            data = []
            for l in table_lines[1:]:
                row = [c.strip() for c in l.split('|') if c.strip()]
                if len(row) == len(header) and all(re.match(r'^[1-5](?:\.\d+)?$', c) for c in row[1:]):
                    data.append(row)
            if not data or len(header) < 2:
                return None, None
            try:
                df = pd.DataFrame(data, columns=header)
                for col in df.columns[1:]:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                return df.iloc[:, 0], df.iloc[:, 1:]
            except Exception:
                return None, None
        ide_col, df_scores = extract_scores_from_table(hasil_perbandingan)
        # Ambil label ide yang dipilih di Tab 2
        selected_labels = st.session_state.get('compare_selected', None)
        if df_scores is not None and not df_scores.empty and selected_labels is not None:
            # Pastikan jumlah bar dan label sesuai ide yang dipilih
            ide_labels = list(selected_labels)
            mean_scores = df_scores.mean(axis=1)
            # Jika jumlah mean_scores tidak sama dengan jumlah ide_labels, sesuaikan
            if len(mean_scores) > len(ide_labels):
                mean_scores = mean_scores[:len(ide_labels)]
            elif len(mean_scores) < len(ide_labels):
                ide_labels = ide_labels[:len(mean_scores)]
            # Ubah label sumbu X menjadi 2 kata pertama + '...'
            def short_label(label):
                words = label.split()
                if len(words) > 2:
                    return ' '.join(words[:2]) + '...'
                return label
            short_labels = [short_label(label) for label in ide_labels]
            bar_colors = plt.cm.Paired(np.linspace(0, 1, len(short_labels)))
            fig, ax = plt.subplots(figsize=(6, 3.5))  # smaller chart
            bars = ax.bar(short_labels, mean_scores, color=bar_colors, width=0.6)
            ax.set_ylabel('Rata-rata Skor', fontsize=11)
            ax.set_xlabel('Ide', fontsize=11)
            ax.set_title('Rata-rata Skor per Ide', fontsize=13, pad=10)
            ax.set_xticks(np.arange(len(short_labels)))
            ax.set_xticklabels(short_labels, rotation=15, ha='right', fontsize=10, wrap=True)
            ax.tick_params(axis='y', labelsize=10)
            ax.tick_params(axis='x', labelsize=10)
            for i, (bar, score) in enumerate(zip(bars, mean_scores)):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f"{score:.2f}", ha='center', va='bottom', fontsize=9)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_alpha(0.5)
            ax.spines['bottom'].set_alpha(0.5)
            ax.grid(axis='y', linestyle='--', alpha=0.15)
            fig.tight_layout(pad=1.2)
            st.pyplot(fig)
            # Kesimpulan rata-rata tertinggi (bisa lebih dari 1)
            max_score = mean_scores.max()
            best_idxs = [i for i, v in enumerate(mean_scores) if np.isclose(v, max_score)]
            if len(best_idxs) == 1:
                st.success(f"Ide dengan rata-rata skor kriteria tertinggi: **{ide_labels[best_idxs[0]]}** (skor rata-rata {mean_scores[best_idxs[0]]:.2f})")
            else:
                best_names = ', '.join(f'**{ide_labels[i]}**' for i in best_idxs)
                st.info(f"Ada {len(best_idxs)} ide dengan rata-rata skor kriteria tertinggi: {best_names} (skor rata-rata {max_score:.2f})")
            st.caption("Bar chart di atas menunjukkan rata-rata skor seluruh kriteria untuk masing-masing ide. Semakin tinggi batang, semakin unggul ide tersebut secara keseluruhan.")
            # Saran berdasarkan kriteria favorit user ATAU kriteria tertinggi per ide jika tidak ada kriteria tambahan
            if 'kriteria_list' in locals() and kriteria_list:
                # Cari kriteria favorit user (selain default)
                kriteria_favorit = None
                for k in reversed(kriteria_list):
                    if k not in ["Potensi Pasar", "Kesulitan Implementasi", "Inovasi", "Modal Awal"]:
                        kriteria_favorit = k
                        break
                if kriteria_favorit and kriteria_favorit in df_scores.columns:
                    skor_kriteria = df_scores[kriteria_favorit]
                    max_krit = skor_kriteria.max()
                    best_krit_idxs = [i for i, v in enumerate(skor_kriteria) if np.isclose(v, max_krit)]
                    if len(best_krit_idxs) == 1:
                        st.info(f"Jika Anda lebih mementingkan kriteria **{kriteria_favorit}**, maka ide yang paling cocok adalah: **{ide_labels[best_krit_idxs[0]]}** (skor {max_krit:.2f} pada kriteria tersebut).")
                    else:
                        best_krit_names = ', '.join(f'**{ide_labels[i]}**' for i in best_krit_idxs)
                        st.info(f"Jika Anda lebih mementingkan kriteria **{kriteria_favorit}**, maka ide yang paling cocok adalah: {best_krit_names} (skor {max_krit:.2f} pada kriteria tersebut).")
                else:
                    # Tidak ada kriteria tambahan user, buat saran berdasarkan kriteria tertinggi per ide
                    if len(best_idxs) > 1:
                        st.write(f"Kesimpulan : Dari hasil perhitungan kami, ada {len(best_idxs)} ide dengan nilai rata-rata dan skor kriteria tertinggi yang setara. Kami menyarankan untuk melakukan analisis lebih mendalam, seperti diskusi tim atau evaluasi tambahan terhadap faktor seperti dampak, biaya, atau kemudahan implementasi, sebelum menentukan pilihan akhir.")
                    else:
                        # Hanya satu ide terbaik, tampilkan saran biasa
                        st.write(f"Kami menyimpulkan jika Ide **{ide_labels[best_idxs[0]]}** telah melalui proses evaluasi, ide ini terbukti memiliki nilai rata-rata paling tinggi di antara semua alternatif yang dipertimbangkan, sekaligus meraih skor kriteria tertinggi dalam aspek-aspek penilaian seperti inovasi, kelayakan, dan dampak potensial.")

