# EduBot Telegram

EduBot adalah chatbot Telegram untuk mencari info beasiswa dan mengingatkan deadline tugas.

## Fitur
- Cari info beasiswa terbaru (/beasiswa)
- Reminder deadline tugas (/reminder)

## Tech Stack
- Python
- BeautifulSoup (web scraping)
- Telegram Bot API
- GitHub Actions (scheduler)

## Cara Menjalankan Lokal
1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
2. Buat bot di @BotFather, dapatkan token, lalu set environment variable:
   ```powershell
   $env:TELEGRAM_BOT_TOKEN="<TOKEN_BOT_ANDA>"
   ```
3. Jalankan bot:
   ```powershell
   python bot.py
   ```

## Deployment Otomatis
- Gunakan GitHub Actions untuk menjalankan bot/scraper secara terjadwal.
- Simpan token di GitHub Secrets.
