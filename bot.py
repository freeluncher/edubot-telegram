import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import edubot.scraper

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Halo! Saya EduBot. Ketik /beasiswa untuk info beasiswa, /reminder untuk atur pengingat.')

async def beasiswa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = edubot.scraper.get_beasiswa_info()
    await update.message.reply_text(info)

def main():
    # Token akan diambil dari environment variable (GitHub Secret)
    import os
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise Exception('TELEGRAM_BOT_TOKEN belum diatur di environment variable.')
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('beasiswa', beasiswa))
    # Handler lain akan ditambahkan di sini
    app.run_polling()

if __name__ == '__main__':
    main()
