import requests
from bs4 import BeautifulSoup
import json
import os

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

response = requests.get(url)
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "lxml")

books = []
items = soup.select("article.product_pod")

for item in items:
    title = item.h3.a["title"]
    price = item.select_one(".price_color").text
    stock = item.select_one(".instock.availability").text.strip()
    link = item.h3.a["href"]

    books.append({
        "title": title,
        "price": price,
        "stock": stock,
        "link": "https://books.toscrape.com/catalogue/" + link
    })

for book in books:
    print(book)

output_file = "books_data.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=4)

print(f"\n 已儲存 {len(books)} 筆資料到 {output_file}")
print(f"檔案位置：{os.path.abspath(output_file)}")
