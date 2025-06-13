import os
import json
from datetime import datetime, timedelta
import requests

REMINDER_FILE = os.path.join(os.path.dirname(__file__), 'edubot', 'reminder_data.json')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

def send_reminder(user_id, text):
    data = {
        'chat_id': user_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    requests.post(API_URL, data=data)

def main():
    if not TELEGRAM_BOT_TOKEN:
        print('TELEGRAM_BOT_TOKEN belum diatur di environment variable.')
        return
    if not os.path.exists(REMINDER_FILE):
        print('Belum ada data reminder.')
        return
    with open(REMINDER_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    today = datetime.now().date()
    besok = today + timedelta(days=1)
    for user_id, reminders in data.items():
        pesan = ''
        for r in reminders:
            try:
                deadline = datetime.strptime(r['deadline'], '%Y-%m-%d').date()
            except Exception:
                continue
            if deadline == today:
                pesan += f"⚠️ <b>Deadline hari ini:</b> <b>{r['title']}</b> ({r['deadline']})\n"
            elif deadline == besok:
                pesan += f"⏰ <b>Deadline besok:</b> <b>{r['title']}</b> ({r['deadline']})\n"
        if pesan:
            send_reminder(user_id, pesan)

if __name__ == '__main__':
    main()
