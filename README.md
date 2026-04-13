# Alkitab Teman Hati (MVP)

Webapp + Telegram bot berbahasa Indonesia yang merespons curhat pengguna seperti "teman refleksi rohani" (bukan pengganti terapis profesional), lalu memberi rekomendasi ayat/passage Alkitab (TB) dan rencana baca personal.

## Tujuan Produk
- Pengguna menulis perasaan/masalah (cemas, putus asa, marah, bingung, dll).
- Sistem melakukan klasifikasi emosi + tema rohani.
- Sistem mengembalikan:
  1. validasi emosi yang empatik,
  2. 1-3 ayat/passage TB yang relevan,
  3. refleksi singkat,
  4. rencana baca 3-7 hari yang disesuaikan.

## Prinsip Safety
- Tidak mengklaim sebagai terapis berlisensi.
- Menampilkan dislaimer dan escalation message untuk self-harm / kekerasan.
- Menolak memberi diagnosis klinis.
- Menyarankan bantuan profesional jika ada risiko tinggi.

## Arsitektur MVP
- **Client**: Telegram Bot + web chat sederhana.
- **API**: FastAPI (`/chat`, `/telegram/webhook`).
- **NLP layer**:
  - sentiment + emotion tagging (rule-based dulu, bisa upgrade ke LLM).
  - retrieval ayat berbasis tag (`cemas`, `takut`, `pengampunan`, dst).
- **Data**:
  - indeks ayat TB (JSON/SQLite + tag tematik).
  - log percakapan dan reading plan per user.
- **Scheduler**: job harian untuk kirim ayat lanjutan via Telegram.

## Alur Respons
1. Terima input pengguna.
2. Jalankan `detect_emotion` dan `detect_theme`.
3. Ambil ayat paling relevan dari indeks TB.
4. Bangun respons empatik + refleksi.
5. Simpan konteks user dan update rencana baca.

## Stack yang disarankan
- Python 3.11+
- FastAPI + Uvicorn
- python-telegram-bot
- SQLite/Postgres

## Menjalankan MVP
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Endpoint
- `GET /health`
- `POST /chat`
- `POST /telegram/webhook`

## Catatan lisensi teks Alkitab
Pastikan Anda memiliki izin legal untuk distribusi teks "Alkitab Terjemahan Baru" dari pemegang hak terkait. Untuk development awal, gunakan data dummy/sampel terlebih dahulu.
