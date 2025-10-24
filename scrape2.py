# scrape2.py
import requests
from bs4 import BeautifulSoup
import json

URL = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

resp = requests.get(URL, timeout=10)
resp.raise_for_status()

soup = BeautifulSoup(resp.content, "lxml")

books = []
articles = soup.find_all("article", class_="product_pod")
for art in articles:
    a = art.find("h3").find("a")
    title = a.get("title", "").strip()

    price_tag = art.find("p", class_="price_color")
    price = price_tag.get_text(strip=True) if price_tag else ""

    rating_tag = art.find("p", class_="star-rating")
    rating = "Unknown"
    if rating_tag:
        classes = rating_tag.get("class", [])
        for c in classes:
            if c != "star-rating":
                rating = c

    books.append({
        "title": title,
        "price": price,
        "rating": rating
    })

print(books)
print(json.dumps(books, ensure_ascii=False, indent=2))