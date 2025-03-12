# AbsenKuy Bot

Bot Telegram untuk presensi otomatis mahasiswa AMIKOM Purwokerto.

## Fitur

- ✅ Login ke portal mahasiswa
- 📋 Melihat daftar presensi yang tersedia
- 📝 Melakukan presensi otomatis
- 📊 Melihat informasi profil mahasiswa
- 🔄 Logout dari sistem

## Teknologi

- Python 3.8+
- python-telegram-bot 20.8
- requests 2.31.0
- BeautifulSoup4 4.12.2
- python-dotenv 1.0.0

## Instalasi

1. Clone repositori ini
   ```bash
   git clone https://github.com/username/absenkuy-bot.git
   cd absenkuy-bot
   ```

2. Buat virtual environment
   ```bash
   python -m venv venv
   ```

3. Aktifkan virtual environment
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Install dependensi
   ```bash
   pip install -r requirements.txt
   ```

5. Salin file `.env.example` menjadi `.env`
   ```bash
   cp .env.example .env
   ```

6. Edit file `.env` dan isi:
   - `TELEGRAM_BOT_TOKEN`: Token bot Telegram dari BotFather
   - `BASE_URL`: URL portal mahasiswa

## Penggunaan

1. Jalankan bot
   ```bash
   python main.py
   ```

2. Di Telegram, mulai obrolan dengan bot dan gunakan perintah:
   - `/start` - Memulai bot
   - `/help` - Melihat daftar perintah
   - `/login` - Login ke portal mahasiswa
   - `/absenbang` - Melihat dan melakukan presensi
   - `/logout` - Logout dari portal

## Struktur Proyek

```
absenkuy-bot/
├── bot/
│   ├── __init__.py
│   ├── bot.py          # Konfigurasi bot Telegram
│   ├── handlers.py     # Handler untuk perintah bot
│   └── student_api.py  # API untuk portal mahasiswa
├── main.py             # File utama untuk menjalankan bot
├── requirements.txt    # Dependensi
├── .env.example        # Contoh file konfigurasi
└── README.md           # Dokumentasi
```

## Keamanan

- Jangan share file `.env` yang berisi token bot
- Gunakan fitur ini dengan bertanggung jawab
- Bot ini hanya bisa digunakan untuk akun Anda sendiri

## Lisensi

MIT License 