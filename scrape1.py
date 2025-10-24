# scrape1.py
import requests
import re

URL = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

resp = requests.get(URL, timeout=10)
resp.raise_for_status()

html = resp.text

pattern = r'£\d+\.\d{2}'
prices = re.findall(pattern, html)

print(prices)