# Modul reminder deadline tugas akan dibuat di sini

import json
from datetime import datetime
import os

REMINDER_FILE = os.path.join(os.path.dirname(__file__), 'reminder_data.json')

def load_reminders(user_id):
    if not os.path.exists(REMINDER_FILE):
        return []
    with open(REMINDER_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get(str(user_id), [])

def save_reminders(user_id, reminders):
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}
    data[str(user_id)] = reminders
    with open(REMINDER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_reminder(user_id, title, deadline):
    reminders = load_reminders(user_id)
    reminders.append({'title': title, 'deadline': deadline})
    save_reminders(user_id, reminders)

def get_reminders(user_id):
    reminders = load_reminders(user_id)
    if not reminders:
        return 'Belum ada deadline tugas yang disimpan.'
    reminders.sort(key=lambda x: x['deadline'])
    result = 'Daftar deadline tugas Anda:\n'
    for r in reminders:
        result += f"- {r['title']} (deadline: {r['deadline']})\n"
    return result

def parse_deadline(text):
    try:
        # Format: YYYY-MM-DD
        dt = datetime.strptime(text, '%Y-%m-%d')
        return dt.strftime('%Y-%m-%d')
    except Exception:
        return None

def delete_reminder(user_id, title):
    reminders = load_reminders(user_id)
    new_reminders = [r for r in reminders if r['title'].lower() != title.lower()]
    if len(new_reminders) == len(reminders):
        return False
    save_reminders(user_id, new_reminders)
    return True

def edit_reminder(user_id, old_title, new_title, new_deadline):
    reminders = load_reminders(user_id)
    found = False
    for r in reminders:
        if r['title'].lower() == old_title.lower():
            r['title'] = new_title
            r['deadline'] = new_deadline
            found = True
            break
    if found:
        save_reminders(user_id, reminders)
        return True
    return False
