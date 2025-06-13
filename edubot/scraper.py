# Modul scraping beasiswa akan dibuat di sini
import requests
from bs4 import BeautifulSoup

def get_beasiswa_info():
    # Contoh scraping: ambil 3 beasiswa terbaru dari website beasiswa populer
    url = 'https://www.beasiswapascasarjana.com/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Ambil 3 beasiswa terbaru dari judul dengan selector: h3 > a
        items = soup.select('h3 > a')[:3]
        if not items:
            # Fallback: cari judul dengan selector h2 > a
            items = soup.select('h2 > a')[:3]
        if not items:
            return 'Maaf, info beasiswa tidak ditemukan.'
        hasil = 'Beasiswa terbaru:\n'
        for item in items:
            judul = item.get_text(strip=True)
            link = item['href']
            hasil += f'- {judul}\n{link}\n'
        return hasil
    except Exception as e:
        return f'Gagal mengambil info beasiswa: {e}'
