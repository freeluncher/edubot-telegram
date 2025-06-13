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
        '/hapusreminder Judul_Tugas - Menghapus reminder berdasarkan judul\n'
        '/editreminder Judul_Lama Judul_Baru YYYY-MM-DD - Mengedit reminder\n'
        '/help - Menampilkan bantuan ini\n\n'
        '<b>Contoh:</b>\n/reminder Tugas Matematika 2025-06-20\n/reminder Tugas Bahasa Inggris 2025-07-15\n\n'
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

async def hapusreminder_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text('Format: /hapusreminder Judul_Tugas', parse_mode='HTML')
        return
    title = ' '.join(context.args)
    if reminder.delete_reminder(user_id, title):
        await update.message.reply_text(f'✅ Reminder <b>{title}</b> berhasil dihapus.', parse_mode='HTML')
    else:
        await update.message.reply_text(f'Reminder <b>{title}</b> tidak ditemukan.', parse_mode='HTML')

async def editreminder_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if len(context.args) < 3:
        await update.message.reply_text('Format: /editreminder Judul_Lama Judul_Baru YYYY-MM-DD', parse_mode='HTML')
        return
    old_title = context.args[0]
    new_title = ' '.join(context.args[1:-1])
    new_deadline = context.args[-1]
    deadline_fmt = reminder.parse_deadline(new_deadline)
    if not deadline_fmt:
        await update.message.reply_text('Format tanggal salah. Gunakan YYYY-MM-DD.', parse_mode='HTML')
        return
    if reminder.edit_reminder(user_id, old_title, new_title, deadline_fmt):
        await update.message.reply_text(f'✅ Reminder <b>{old_title}</b> berhasil diubah menjadi <b>{new_title}</b> ({deadline_fmt})', parse_mode='HTML')
    else:
        await update.message.reply_text(f'Reminder <b>{old_title}</b> tidak ditemukan.', parse_mode='HTML')

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
    app.add_handler(CommandHandler('hapusreminder', hapusreminder_command))
    app.add_handler(CommandHandler('editreminder', editreminder_command))
    app.add_handler(CommandHandler('help', help_command))
    # Handler lain akan ditambahkan di sini
    app.run_polling()

if __name__ == '__main__':
    main()
