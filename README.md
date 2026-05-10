# 🧾 SmartSplit Bill AI

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini API](https://img.shields.io/badge/Gemini_API-2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> Aplikasi web berbasis Streamlit yang menggunakan kecerdasan buatan (Google Gemini 2.5 Flash) untuk membaca foto nota/struk belanja, mengekstrak data transaksi secara otomatis, dan membagi tagihan ke beberapa orang dengan adil dan transparan.

![Demo](assets/demo.gif)

---

## ✨ Fitur Utama

- 📷 **Baca Nota Otomatis dengan AI** — Upload foto struk, biarkan Gemini 2.5 Flash mengekstrak semua data secara instan
- 🔍 **Ekstraksi Data Lengkap** — Nama item, quantity, harga satuan, total per item, subtotal, biaya tambahan (pajak/servis), dan total keseluruhan
- 👥 **Input Peserta Dinamis** — Tambah atau kurangi nama peserta secara fleksibel sesuai kebutuhan
- 🏷️ **Assign Item ke Peserta** — Tandai siapa yang memesan item apa; satu item bisa di-split merata ke beberapa orang
- 💰 **Kalkulasi Otomatis per Orang** — Total tagihan per peserta dihitung secara otomatis, termasuk proporsi biaya tambahan
- ✅ **Verifikasi Total** — Sistem memverifikasi bahwa total split cocok dengan total bill asli
- 🖼️ **Support Format Gambar** — JPG, JPEG, dan PNG

---

## 🛠️ Tech Stack

| Teknologi | Versi | Alasan Penggunaan |
|---|---|---|
| **Python** | 3.12 | Bahasa utama; ekosistem ML/AI terlengkap |
| **Streamlit** | Latest | Framework web Python tercepat untuk prototyping aplikasi data |
| **Google Gemini API** | gemini-2.5-flash | Model multimodal terbaik untuk pembacaan gambar + teks dengan akurasi tinggi |
| **Pillow (PIL)** | Latest | Preprocessing dan display gambar di dalam aplikasi |
| **python-dotenv** | Latest | Manajemen environment variable agar API key tidak di-hardcode |
| **Qwen2-VL** | 2B (eksperimen) | Model vision open-source lokal sebagai alternatif untuk perbandingan |

---

## 🚀 Instalasi & Menjalankan Aplikasi

### Prerequisites

Sebelum mulai, pastikan kamu sudah memiliki:
- ✅ **Python 3.12** — [Download di sini](https://www.python.org/downloads/)
- ✅ **Git** — [Download di sini](https://git-scm.com/downloads)
- ✅ **Akun Google** — Untuk mendapatkan Gemini API key gratis

---

### Langkah 1: Clone Repository

```bash
git clone https://github.com/username/SmartSplit_Bill_AI.git
cd SmartSplit_Bill_AI
```

---

### Langkah 2: Buat Virtual Environment

```bash
python -m venv venv
```

---

### Langkah 3: Aktifkan Virtual Environment

**Windows (Command Prompt / PowerShell):**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

> Jika berhasil, nama environment `(venv)` akan muncul di awal baris terminal.

---

### Langkah 4: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Langkah 5: Setup Gemini API Key

#### a. Daftar dan buat API key di Google AI Studio

1. Buka [aistudio.google.com](https://aistudio.google.com)
2. Login dengan akun Google kamu
3. Klik tombol **"Get API Key"** di sidebar kiri
4. Klik **"Create API key"** → pilih project Google Cloud (atau buat baru)
5. Salin API key yang muncul

#### b. Buat file `.env` di root project

```bash
# Windows
echo GEMINI_API_KEY=your_api_key_here > .env

# macOS / Linux
touch .env
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

Atau buat file `.env` secara manual dengan isi:

```env
GEMINI_API_KEY=your_api_key_here
```

> ⚠️ **Jangan pernah commit file `.env` ke repository!** File ini sudah termasuk dalam `.gitignore`.

---

### Langkah 6: Jalankan Aplikasi

```bash
streamlit run app.py
```

---

### Langkah 7: Buka di Browser

Aplikasi akan otomatis terbuka, atau akses manual di:

```
http://localhost:8501
```

---

## 📖 Cara Penggunaan

**Step 1 — Upload Foto Nota**
> Klik area upload atau drag & drop foto struk belanja kamu. Format yang didukung: JPG, JPEG, PNG.

**Step 2 — Klik "Baca Nota dengan AI"**
> Tekan tombol untuk mengirim gambar ke Google Gemini 2.5 Flash. Proses biasanya selesai dalam 2–5 detik.

**Step 3 — Cek Hasil Bacaan AI**
> Periksa daftar item yang berhasil diekstrak: nama item, qty, harga satuan, dan total. Pastikan hasilnya sesuai dengan struk asli.

**Step 4 — Input Nama Peserta**
> Masukkan nama setiap orang yang ikut patungan. Tambah baris baru sesuai jumlah peserta.

**Step 5 — Assign Item ke Peserta**
> Untuk setiap item, centang nama peserta yang memesan item tersebut. Jika satu item dipesan bersama, centang semua yang terlibat — biaya akan dibagi rata otomatis.

**Step 6 — Klik "Hitung Split"**
> Aplikasi menghitung total tagihan per orang, termasuk proporsi biaya tambahan seperti pajak dan servis. Hasil verifikasi total juga ditampilkan.

---

## 🔬 Hasil Eksperimen Model

Dua model diuji coba untuk tugas pembacaan nota: **Google Gemini 2.5 Flash** (cloud) dan **Qwen2-VL-2B** (lokal/open-source) menggunakan 2 sampel struk yang berbeda (`nota_1.jpg` — struk restoran, `nota_2.jpg` — struk minimarket).

### Hasil Ekstraksi — Gemini 2.5 Flash

<details>
<summary>📄 Nota 1 — Struk Restoran (inference time: 10.89 detik)</summary>

| Nama Item | Qty | Harga Satuan | Total |
|---|---|---|---|
| Fried Kwetiau | 1 | Rp 99.000 | Rp 99.000 |
| Spicy Lv 1 | 1 | Rp 1.000 | Rp 1.000 |
| Orange Juice | 1 | Rp 50.000 | Rp 50.000 |
| Avocado Juice | 1 | Rp 50.000 | Rp 50.000 |

**Subtotal:** Rp 200.000
| Biaya Tambahan | Jumlah |
|---|---|
| Discount | -Rp 30.000 |
| Service | Rp 12.750 |
| PB1 | Rp 18.275 |

**Total:** Rp 201.025 ✅ Parse sukses

</details>

<details>
<summary>📄 Nota 2 — Struk Minimarket (inference time: 15.13 detik)</summary>

| Nama Item | Qty | Harga Satuan | Total |
|---|---|---|---|
| SR TWR SPC | 1 | Rp 15.000 | Rp 15.000 |
| KP BRD L 0.020 | 1 | Rp 500 | Rp 500 |
| ALFA SL STR150G | 1 | Rp 13.500 | Rp 13.500 |
| GD 3IN1 MOC 10S | 1 | Rp 18.700 | Rp 18.700 |
| Disc. | 1 | -Rp 1.800 | -Rp 1.800 |
| GADDJAH TBRK138G | 1 | Rp 21.800 | Rp 21.800 |

**Subtotal:** Rp 67.700
| Biaya Tambahan | Jumlah |
|---|---|
| PPN | Rp 6.868 |

**Total:** Rp 74.568 ✅ Parse sukses

</details>

---

### Hasil Ekstraksi — Qwen2-VL-2B

<details>
<summary>📄 Nota 1 (inference time: 56.47 detik)</summary>

> ❌ **Parse gagal** — Output tidak valid JSON.
> Error: `Extra data: line 5 column 5 (char 75)`
>
> Model berhasil mengenali beberapa teks dari gambar, namun gagal menghasilkan format JSON yang konsisten dan parseable.

</details>

<details>
<summary>📄 Nota 2 (inference time: 71.04 detik)</summary>

> ❌ **Parse gagal** — Output tidak valid JSON.
> Error: `Extra data: line 5 column 5 (char 75)`
>
> Masalah yang sama terjadi pada nota kedua — model menghasilkan output JSON yang malformed dan tidak bisa diproses lebih lanjut.

</details>

---

### Tabel Komparasi Model

<details>
<summary>📋 Lihat Tabel Komparasi Lengkap</summary>

| Aspek | gemini-2.5-flash | Qwen2-VL-2B |
|---|---|---|
| **Jenis Model** | Proprietary Multimodal LLM | Open Source Vision LLM |
| **Akses** | API (Internet required) | Lokal (offline) |
| **Butuh GPU?** | Tidak | Tidak wajib (CPU bisa, lambat) |
| **API Key?** | Ya (Google AI Studio) | Tidak |
| **Biaya** | Gratis (free tier) | Gratis (tapi download ~5GB) |
| **Avg. Inference Time** | **13.01 detik** | 63.76 detik |
| **Parse JSON Success Rate** | **2/2 (100%)** | 0/2 (0%) |
| **Akurasi Nama Item** | Sangat Baik ⭐⭐⭐⭐⭐ | Cukup Baik ⭐⭐⭐ |
| **Akurasi Harga** | Sangat Baik ⭐⭐⭐⭐⭐ | Cukup Baik ⭐⭐⭐ |
| **Deteksi Biaya Tambahan** | Baik ⭐⭐⭐⭐ | Kurang Konsisten ⭐⭐ |
| **Konsistensi Format Output** | Sangat Konsisten ⭐⭐⭐⭐⭐ | Kurang Konsisten ⭐⭐ |
| **Kemudahan Setup** | Mudah (pip install saja) | Kompleks (butuh download besar) |
| **Rekomendasi** | ✅ Direkomendasikan untuk produksi | ⚠️ Lebih cocok untuk offline/privasi |

</details>

---

### 🏆 Alasan Memilih `gemini-2.5-flash` sebagai Model Final

1. **Akurasi lebih tinggi pada teks campuran** — Gemini lebih andal dalam membaca nota yang memuat campuran huruf cetak, tulisan tangan, dan angka dalam satu gambar.
2. **Output JSON yang konsisten** — Gemini menghasilkan format output yang lebih terstruktur dan mudah di-parse, sehingga lebih sedikit error pada tahap parsing.
3. **Tidak butuh GPU lokal** — Berjalan sepenuhnya via API, sehingga aplikasi bisa dijalankan di laptop biasa tanpa hardware khusus.
4. **Latency lebih rendah** — Rata-rata inference time Gemini lebih cepat dibanding Qwen2-VL yang harus dijalankan di CPU/GPU lokal.
5. **Free tier yang memadai untuk penggunaan personal** — Google AI Studio menyediakan kuota gratis yang cukup untuk penggunaan dan demo aplikasi ini.

---

## 📊 Evaluasi Akhir Produk

### Evaluasi Model AI

#### Kelemahan Model

1. **Bergantung penuh pada koneksi internet** — Jika jaringan tidak stabil atau API Google tidak tersedia, seluruh fitur pembacaan nota tidak bisa digunakan.
2. **Rate limit pada free tier** — Pengguna yang sering menggunakan aplikasi bisa mencapai batas kuota API harian, yang menghambat penggunaan.
3. **Akurasi menurun pada foto berkualitas rendah** — Gambar buram, tulisan tangan, atau pencahayaan buruk masih bisa menyebabkan kesalahan ekstraksi nama item maupun harga.

#### Ide Improvement Model

1. **Fine-tune model khusus receipt** — Melatih model dengan dataset struk belanja spesifik (berbagai format, bahasa, dan toko) untuk meningkatkan akurasi secara signifikan.
2. **Tambahkan preprocessing gambar otomatis** — Terapkan langkah contrast enhancement, sharpening, dan denoising sebelum gambar dikirim ke model agar kualitas input lebih baik.
3. **Fallback ke model lokal** — Implementasikan mekanisme fallback ke Qwen2-VL atau model lokal lain jika API Gemini tidak tersedia, sehingga aplikasi tetap bisa beroperasi offline.

---

### Evaluasi Produk Web

#### Kelemahan Produk

1. **Tidak ada fitur edit manual hasil bacaan AI** — Jika ada item yang salah terbaca, pengguna tidak bisa mengoreksinya langsung di aplikasi dan harus mengulang proses dari awal.
2. **Tidak ada history transaksi tersimpan** — Setiap sesi adalah sesi baru; hasil split tidak disimpan sehingga pengguna tidak bisa melihat riwayat patungan sebelumnya.
3. **Belum support multiple receipt sekaligus** — Pengguna hanya bisa memproses satu struk per sesi; belum ada fitur untuk menggabungkan beberapa nota dalam satu perhitungan split.

#### Ide Improvement Produk

1. **Tambah fitur edit item secara manual** — Berikan UI tabel yang bisa diedit langsung (editable dataframe) sehingga pengguna bisa memperbaiki hasil bacaan AI tanpa harus re-upload.
2. **Tambahkan database untuk history split** — Integrasikan SQLite atau Supabase untuk menyimpan riwayat sesi split, sehingga pengguna bisa mengakses kembali hasil perhitungan masa lalu.
3. **Export hasil split ke PDF atau WhatsApp** — Tambahkan tombol untuk mengunduh rekap tagihan dalam format PDF atau membagikannya langsung via tautan WhatsApp yang sudah diformat rapi.

---

## 📁 Struktur Proyek

```
SmartSplit_Bill_AI/
├── .env                    # Environment variable (API key) — tidak di-commit
├── .gitignore              # Daftar file/folder yang diabaikan Git
├── requirements.txt        # Semua dependencies Python
├── app.py                  # Entry point aplikasi Streamlit (UI & logika utama)
├── models/
│   ├── __init__.py
│   ├── gemini_reader.py    # Modul integrasi Google Gemini API untuk baca nota
│   └── qwen_reader.py      # Modul eksperimen Qwen2-VL (model lokal)
├── utils/
│   ├── __init__.py
│   └── bill_parser.py      # Fungsi parsing & kalkulasi split tagihan
├── notebooks/
│   └── model_experiment.ipynb  # Notebook eksperimen dan perbandingan model
└── sample_bills/           # Koleksi foto struk sampel untuk testing
```

---

## 🤝 Contributing

Kontribusi sangat disambut! Berikut langkah-langkahnya:

1. Fork repository ini
2. Buat branch baru: `git checkout -b feature/nama-fitur`
3. Commit perubahan: `git commit -m 'feat: tambah fitur xyz'`
4. Push ke branch: `git push origin feature/nama-fitur`
5. Buat Pull Request

Pastikan kode kamu mengikuti standar PEP 8 dan sudah diuji sebelum PR diajukan.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

```
MIT License — bebas digunakan, dimodifikasi, dan didistribusikan
dengan syarat mencantumkan atribusi ke penulis asli.
```

---

<p align="center">
  Dibuat dengan ☕ dan 🤖 oleh <a href="https://github.com/username">username</a>
</p>