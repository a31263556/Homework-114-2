import requests
from bs4 import BeautifulSoup
import json
import re

URL = "https://www.books.com.tw/web/sys_saletopb/books/19?attribute=30"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

resp = requests.get(URL, headers=HEADERS, timeout=10)
resp.raise_for_status()

soup = BeautifulSoup(resp.content, "lxml")

results = []

candidates = soup.select(".mod.type02_list li") or soup.select(".type02_list li") or soup.select(".goodsitem") or soup.select("li")

count = 0
for node in candidates:
    if count >= 20:
        break

    title = ""
    t = node.select_one("h4 a") or node.select_one("a[title]") or node.find("a")
    if t:
        title = t.get("title") or t.get_text(strip=True)

    if not title:
        continue

    price = ""
    ptag = node.select_one(".price") or node.select_one(".b_price") or node.select_one(".price_a") or node.find("span", class_="price")
    if ptag:
        price = ptag.get_text(strip=True)
    else:
        text = node.get_text(" ", strip=True)
        m = re.search(r'NT\$?\s*[\d,]+', text)
        if m:
            price = m.group(0)

    count += 1
    results.append({
        "rank": count,
        "title": title,
        "price": price
    })

print(json.dumps(results, ensure_ascii=False, indent=2))
