# Alkitab Teman Hati (Panduan Non-Programmer)

Kalau kamu tidak bisa coding, tenang — anggap ini seperti:
- **Website chat rohani** (yang bisa langsung dipakai di browser),
- lalu nanti bisa ditambah **bot Telegram**.

---

## Ini webapp atau Telegram bot?
**Keduanya bisa.**
Tapi urutannya yang paling gampang:
1. Jalankan dulu sebagai **webapp**.
2. Setelah itu baru sambungkan ke **Telegram bot**.

---

## Cara paling mudah deploy (tanpa ngoding server): pakai Render
Render itu layanan hosting. Kamu cukup klik-klik.

### Step 1 — Simpan project ke GitHub
Kalau belum punya akun GitHub:
1. Buka https://github.com dan daftar.
2. Buat repository baru (misalnya: `alkitab-teman-hati`).
3. Upload isi folder project ini ke repository itu.

### Step 2 — Deploy ke Render
1. Buka https://render.com dan login (boleh pakai akun GitHub).
2. Klik **New +** → **Web Service**.
3. Pilih repository GitHub kamu.
4. Isi pengaturan ini:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Klik **Create Web Service**.

Tunggu 2–5 menit sampai status jadi **Live**.

### Step 3 — Buka aplikasinya
Render akan kasih link seperti:
`https://nama-app-kamu.onrender.com`

Buka link itu di browser. Kamu akan melihat halaman chat “Alkitab Teman Hati”.

---

## Cara test (versi non-teknis)
Setelah website live:
1. Buka halaman webapp.
2. Tulis curhat singkat, contoh:
   - “Saya cemas soal masa depan.”
3. Klik tombol **Kirim Curhat**.
4. Harus muncul:
   - refleksi singkat,
   - ayat rekomendasi,
   - rencana baca.

Kalau itu muncul, berarti aplikasi **berjalan normal**.

---

## Kalau kamu ingin jalankan di laptop sendiri (opsional)
Ini versi teknis (boleh dibantu orang):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Lalu buka `http://localhost:8000`.

---

## Telegram bot kapan?
Setelah webapp online stabil, baru lanjut:
1. Buat bot via **@BotFather** di Telegram.
2. Dapat token bot.
3. Hubungkan webhook bot ke:
   `https://domain-kamu/telegram/webhook`

Saat ini endpoint webhook sudah ada, jadi pondasinya siap.

---

## File penting di project ini
- `app/main.py` → “mesin” aplikasi.
- `templates/index.html` → tampilan web.
- `data/alkitab_tb_sample.json` → data ayat contoh.

---

## Catatan lisensi
Untuk pakai teks penuh “Alkitab Terjemahan Baru”, pastikan izin lisensinya sesuai dari pemegang hak terkait.
