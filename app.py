import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
from models.gemini_reader import read_bill_gemini
from utils.bill_parser import validate_bill_data, calculate_split, format_currency
import tempfile
import json

load_dotenv()

st.set_page_config(
    page_title="SmartSplit Bill AI",
    page_icon="🧾",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }

    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

    .person-total {
        background: #f0f7ff;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }

    .badge-success {
        background: #d4edda;
        color: #155724;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🧾 SmartSplit Bill AI</h1>
    <p>Upload nota belanja, AI akan membacanya otomatis, lalu split tagihan ke semua orang!</p>
</div>
""", unsafe_allow_html=True)

if "bill_data" not in st.session_state:
    st.session_state.bill_data = None

if "participants" not in st.session_state:
    st.session_state.participants = []

if "item_assignments" not in st.session_state:
    st.session_state.item_assignments = {}

if "split_result" not in st.session_state:
    st.session_state.split_result = None

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

with st.sidebar:

    st.header("⚙️ Konfigurasi")

    api_key = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password"
    )

    st.divider()

    st.info("💡 Dapatkan API key gratis di [aistudio.google.com](https://aistudio.google.com)")

    st.divider()

    if st.button("🔄 Reset Semua", use_container_width=True):

        st.session_state.bill_data = None
        st.session_state.participants = []
        st.session_state.item_assignments = {}
        st.session_state.split_result = None
        st.session_state.uploaded_image = None

        st.rerun()

st.subheader("📸 Step 1: Upload Foto Nota")

uploaded_file = st.file_uploader(
    "Pilih foto nota/struk belanja",
    type=["jpg", "jpeg", "png"],
    help="Pastikan foto cukup jelas dan fokus"
)

if uploaded_file is not None:

    st.session_state.uploaded_image = uploaded_file

    col1, col2 = st.columns([1, 1])

    with col1:

        image = Image.open(uploaded_file)

        st.image(image, caption="Foto nota yang diupload", use_container_width=True)

    with col2:

        st.write("**Informasi File:**")

        st.write(f"📄 Nama: `{uploaded_file.name}`")

        st.write(f"📦 Ukuran: `{uploaded_file.size / 1024:.1f} KB`")

        st.divider()

        if st.button("🤖 Baca Nota dengan AI", type="primary", use_container_width=True):

            if not api_key:
                st.error("⚠️ Masukkan Gemini API Key di sidebar terlebih dahulu!")

            else:

                with st.spinner("AI sedang membaca nota... mohon tunggu 🔍"):

                    try:

                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".jpg"
                        ) as tmp_file:

                            tmp_file.write(uploaded_file.getvalue())

                            tmp_path = tmp_file.name

                        bill_data = read_bill_gemini(tmp_path, api_key)

                        os.unlink(tmp_path)

                        is_valid, errors = validate_bill_data(bill_data)

                        if is_valid:

                            st.session_state.bill_data = bill_data

                            st.success("✅ Nota berhasil dibaca!")

                        else:

                            st.error("❌ Data dari AI tidak lengkap:")

                            for error in errors:
                                st.write(f"• {error}")

                    except Exception as e:

                        st.error(f"❌ Error: {str(e)}")

if st.session_state.bill_data is not None:

    st.divider()

    st.subheader("📋 Step 2: Hasil Bacaan AI")

    bill = st.session_state.bill_data

    currency = bill.get("currency", "IDR")

    col_meta1, col_meta2 = st.columns(2)

    with col_meta1:
        st.metric("🤖 Model", bill.get("model_used", "-"))

    with col_meta2:
        st.metric("⚡ Waktu Inference", f"{bill.get('inference_time', 0)} detik")

    st.write("---")

    st.write("**🛒 Daftar Item:**")

    for i, item in enumerate(bill.get("items", [])):

        c1, c2, c3, c4 = st.columns([3, 1, 2, 2])

        with c1:
            st.write(f"**{item.get('name', 'Unknown')}**")

        with c2:
            st.write(f"x{item.get('quantity', 1)}")

        with c3:
            st.write(format_currency(item.get('price_per_item', 0), currency))

        with c4:
            st.write(f"**{format_currency(item.get('total_price', 0), currency)}**")

    st.divider()

    col_sum1, col_sum2 = st.columns(2)

    with col_sum1:

        st.write(f"**Subtotal:** {format_currency(bill.get('subtotal', 0), currency)}")

        for charge in bill.get("additional_charges", []):
            st.write(f"**{charge.get('name', 'Charge')}:** {format_currency(charge.get('amount', 0), currency)}")

    with col_sum2:
        st.markdown(f"### Total: {format_currency(bill.get('total', 0), currency)}")

    with st.expander("🔍 Lihat Raw Data JSON dari AI"):
        st.json(bill)

if st.session_state.bill_data is not None:

    st.divider()

    st.subheader("👥 Step 3: Masukkan Nama Peserta")

    col_input, col_btn = st.columns([3, 1])

    with col_input:

        new_name = st.text_input(
            "Nama peserta",
            placeholder="Contoh: Budi, Ani, Rara...",
            label_visibility="collapsed"
        )

    with col_btn:

        if st.button("➕ Tambah", use_container_width=True):

            if new_name.strip():

                if new_name.strip() not in st.session_state.participants:

                    st.session_state.participants.append(new_name.strip())

                    st.rerun()

                else:
                    st.warning("Nama sudah ada!")

            else:
                st.warning("Nama tidak boleh kosong!")

    if st.session_state.participants:

        st.write("**Peserta saat ini:**")

        for i, person in enumerate(st.session_state.participants):

            col_person, col_del = st.columns([4, 1])

            with col_person:
                st.write(f"👤 {i+1}. **{person}**")

            with col_del:

                if st.button("❌", key=f"del_{i}"):

                    st.session_state.participants.pop(i)

                    st.rerun()

if st.session_state.bill_data is not None and len(st.session_state.participants) > 0:

    st.divider()

    st.subheader("🔀 Step 4: Tentukan Siapa Bayar Apa")

    st.info("💡 Pilih nama peserta yang akan membayar setiap item. Bisa lebih dari satu orang (split merata per item).")

    for i, item in enumerate(st.session_state.bill_data.get("items", [])):

        item_name = item.get("name", f"Item {i+1}")

        item_total = item.get("total_price", 0)

        currency = st.session_state.bill_data.get("currency", "IDR")

        st.write(f"**{item_name}** — {format_currency(item_total, currency)}")

        selected_people = st.multiselect(
            f"Siapa yang bayar item ini?",
            options=st.session_state.participants,
            key=f"assign_{i}",
            label_visibility="collapsed"
        )

        st.session_state.item_assignments[i] = selected_people

if st.session_state.bill_data is not None and len(st.session_state.participants) > 0:

    st.divider()

    if st.button("💰 Hitung Split Tagihan!", type="primary", use_container_width=True):

        unassigned = []

        for i, item in enumerate(st.session_state.bill_data.get("items", [])):

            if i not in st.session_state.item_assignments or \
               len(st.session_state.item_assignments[i]) == 0:

                unassigned.append(item.get("name", f"Item {i+1}"))

        if unassigned:

            st.warning(f"⚠️ Item berikut belum di-assign ke siapapun: {', '.join(unassigned)}")

        else:

            split_result = calculate_split(
                st.session_state.bill_data,
                st.session_state.item_assignments
            )

            st.session_state.split_result = split_result

    if st.session_state.split_result is not None:

        st.subheader("🎯 Hasil Split Tagihan")

        currency = st.session_state.bill_data.get("currency", "IDR")

        total_bill = st.session_state.bill_data.get("total", 0)

        split = st.session_state.split_result

        for person, amount in split.items():

            percentage = (amount / total_bill * 100) if total_bill > 0 else 0

            st.metric(
                label=f"👤 {person}",
                value=format_currency(amount, currency),
                delta=f"{percentage:.1f}% dari total"
            )

        st.divider()

        grand_total = sum(split.values())

        bill_total = float(total_bill)

        col_v1, col_v2 = st.columns(2)

        with col_v1:
            st.metric("📊 Total Bill", format_currency(bill_total, currency))

        with col_v2:
            st.metric("✅ Total Terhitung", format_currency(grand_total, currency))

        if abs(grand_total - bill_total) < 1:

            st.success("✅ Total cocok! Tidak ada yang ketinggalan bayar.")

        else:

            diff = bill_total - grand_total

            st.warning(f"⚠️ Ada selisih {format_currency(diff, currency)} — kemungkinan item yang tidak di-assign.")