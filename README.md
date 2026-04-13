# Alkitab Teman Hati (Webapp + Telegram Bot)

Ini sekarang **dua channel sekaligus**:
1. **Webapp**: UI cantik di browser (`/`) untuk curhat dan menerima ayat + rencana baca.
2. **Telegram Bot**: endpoint webhook (`/telegram/webhook`) sudah disiapkan untuk integrasi bot.

Jadi, jawaban untuk pertanyaanmu: **ini bisa jadi webapp dulu, lalu Telegram ditambahkan bertahap**.

## Fitur MVP saat ini
- Input curhat berbahasa Indonesia.
- Respons empatik.
- Rekomendasi 1-3 ayat berbasis tema emosi.
- Rencana baca personal sederhana.
- Disclaimer safety (bukan pengganti profesional kesehatan mental).

## Cara Launch Local (5 menit)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Lalu buka: `http://localhost:8000`

## Cara Test
```bash
pytest -q
```

## Cara Coba API Manual
```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"u1","message":"Saya sedang cemas soal masa depan"}'
```

## Deploy Cepat (Render)
1. Push repo ke GitHub.
2. Buat **Web Service** di Render.
3. Build command:
   ```bash
   pip install -r requirements.txt
   ```
4. Start command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
5. Setelah live, webapp ada di `/`, API ada di `/chat`.

## Telegram Bot (langkah berikut)
1. Buat bot via BotFather, dapatkan token.
2. Set webhook Telegram ke:
   ```
   https://domain-kamu/telegram/webhook
   ```
3. Implement handler pesan Telegram untuk meneruskan text ke logic `chat`.

## Struktur
- `app/main.py` - FastAPI app + logic rekomendasi ayat.
- `templates/index.html` - UI webapp.
- `data/alkitab_tb_sample.json` - data ayat sample bertag tema.
- `tests/test_app.py` - test endpoint utama.

## Catatan lisensi Alkitab TB
Pastikan Anda memiliki izin legal untuk distribusi teks "Alkitab Terjemahan Baru" dari pemegang hak terkait. Untuk development awal, gunakan data dummy/sampel terlebih dahulu.
