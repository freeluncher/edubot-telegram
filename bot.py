import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import edubot.scraper
from edubot import reminder
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Halo! Saya <b>EduBot</b> 🤖\n\nKetik /help untuk melihat semua perintah.',
        parse_mode='HTML')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan = (
        '🤖 <b>EduBot Telegram</b>\n\n'
        '<b>Perintah yang tersedia:</b>\n'
        '/start - Menampilkan sapaan awal\n'
        '/beasiswa - Info 3 beasiswa terbaru\n'
        '/reminder - Lihat semua deadline tugas Anda\n'
        '/reminder Judul_Tugas YYYY-MM-DD - Tambah deadline tugas baru\n'
        '/help - Menampilkan bantuan ini\n\n'
        '<b>Contoh:</b>\n/reminder Tugas Matematika 2025-06-20\n\n'
        'Format tanggal: <b>YYYY-MM-DD</b>\n'
    )
    await update.message.reply_text(pesan, parse_mode='HTML')

async def beasiswa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = edubot.scraper.get_beasiswa_info()
    await update.message.reply_text(f'<b>Info Beasiswa Terbaru:</b>\n\n{info}', parse_mode='HTML')

async def reminder_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.args:
        # Format: /reminder Judul_Tugas YYYY-MM-DD
        if len(context.args) < 2:
            await update.message.reply_text(
                'Format salah.\n<b>Contoh:</b> /reminder Judul_Tugas 2025-06-20',
                parse_mode='HTML')
            return
        title = ' '.join(context.args[:-1])
        deadline = context.args[-1]
        deadline_fmt = reminder.parse_deadline(deadline)
        if not deadline_fmt:
            await update.message.reply_text(
                'Format tanggal salah. Gunakan <b>YYYY-MM-DD</b>, contoh: 2025-06-20',
                parse_mode='HTML')
            return
        reminder.add_reminder(user_id, title, deadline_fmt)
        await update.message.reply_text(
            f'✅ Reminder untuk <b>{title}</b> pada <b>{deadline_fmt}</b> berhasil ditambahkan!',
            parse_mode='HTML')
    else:
        # Tampilkan daftar reminder
        result = reminder.get_reminders(user_id)
        await update.message.reply_text(f'<b>{result}</b>', parse_mode='HTML')

def main():
    # Token akan diambil dari environment variable (GitHub Secret)
    import os
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise Exception('TELEGRAM_BOT_TOKEN belum diatur di environment variable.')
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('beasiswa', beasiswa))
    app.add_handler(CommandHandler('reminder', reminder_command))
    app.add_handler(CommandHandler('help', help_command))
    # Handler lain akan ditambahkan di sini
    app.run_polling()

if __name__ == '__main__':
    main()
