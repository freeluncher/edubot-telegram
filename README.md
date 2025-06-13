# EduBot Telegram

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://core.telegram.org/bots)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-WebScraping-green)](https://www.crummy.com/software/BeautifulSoup/)
[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/<USERNAME>/<REPO>/scheduler.yml?label=Scheduler&logo=github)](../../actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

EduBot adalah chatbot Telegram untuk mencari info beasiswa dan mengingatkan deadline tugas.

## Fitur
- Cari info beasiswa terbaru (/beasiswa, filter & jumlah)
- Reminder deadline tugas (/reminder, /hapusreminder, /editreminder)
- Notifikasi otomatis deadline tugas (via GitHub Actions)

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
- Simpan token di GitHub Secrets dengan nama `TELEGRAM_BOT_TOKEN`.

## Perintah Bot
- `/start` — Sapaan awal
- `/help` — Bantuan & petunjuk
- `/beasiswa [jumlah] [kata_kunci]` — Info beasiswa terbaru, filter & jumlah opsional
- `/reminder [judul] [YYYY-MM-DD]` — Tambah/lihat deadline tugas
- `/hapusreminder [judul]` — Hapus deadline tugas
- `/editreminder [judul_lama] [judul_baru] [YYYY-MM-DD]` — Edit deadline tugas
