# Modul scraping beasiswa akan dibuat di sini
import requests
from bs4 import BeautifulSoup
import re

def get_beasiswa_info(jumlah=3, keyword=None):
    # Contoh scraping: ambil 3 beasiswa terbaru dari website beasiswa populer
    url = 'https://www.beasiswapascasarjana.com/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Ambil 3 beasiswa terbaru dari judul dengan selector: h3 > a
        items = soup.select('h3 > a')
        if not items:
            # Fallback: cari judul dengan selector h2 > a
            items = soup.select('h2 > a')
        beasiswa_list = []
        for item in items:
            judul = item.get_text(strip=True)
            link = item['href']
            if keyword:
                if re.search(keyword, judul, re.IGNORECASE):
                    beasiswa_list.append({'judul': judul, 'link': link})
            else:
                beasiswa_list.append({'judul': judul, 'link': link})
            if len(beasiswa_list) >= jumlah:
                break
        if not beasiswa_list:
            return 'Maaf, info beasiswa tidak ditemukan.'
        hasil = f'Beasiswa terbaru (max {jumlah}):\n'
        for b in beasiswa_list:
            hasil += f"- {b['judul']}\n{b['link']}\n"
        return hasil
    except Exception as e:
        return f'Gagal mengambil info beasiswa: {e}'
