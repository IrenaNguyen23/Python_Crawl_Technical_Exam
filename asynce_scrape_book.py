import aiohttp
import asyncio
from bs4 import BeautifulSoup
import csv
import os
import aiofiles

BASE_URL = "https://books.toscrape.com/catalogue/category/books/science_22/"
NUM_PAGES = 3

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.text()

def get_star_rating(star_str):
    stars = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return stars.get(star_str, 0)

async def scrape_book(session, book):
    title = book.h3.a["title"]
    price = book.select_one(".price_color").text.strip()
    availability = book.select_one(".availability").text.strip()
    rel_link = book.h3.a["href"].replace("../", "")
    product_url = f"https://books.toscrape.com/catalogue/{rel_link}"

    html = await fetch(session, product_url)

    # Save raw HTML async
    file_name = f"html_backup/{title.replace('/', '-')[:50]}.html"
    async with aiofiles.open(file_name, "w", encoding="utf-8") as f:
        await f.write(html)

    soup = BeautifulSoup(html, "html.parser")
    star_class = soup.select_one("p.star-rating")["class"][1]
    star_rating = get_star_rating(star_class)

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "product_page": product_url,
        "star_rating": star_rating
    }

async def scrape_page(session, page_num):
    if page_num == 1:
        url = BASE_URL + "index.html"
    else:
        url = BASE_URL + f"page-{page_num}.html"

    print(f"Scraping page: {url}")
    html = await fetch(session, url)
    soup = BeautifulSoup(html, "html.parser")
    books = soup.select("article.product_pod")

    tasks = [scrape_book(session, book) for book in books]
    return await asyncio.gather(*tasks)

async def main():
    os.makedirs("html_backup", exist_ok=True)
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_page(session, i) for i in range(1, NUM_PAGES + 1)]
        results = await asyncio.gather(*tasks)

        all_books = [book for page in results for book in page]

        # Save CSV
        with open("books.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "price", "availability", "product_page", "star_rating"])
            writer.writeheader()
            writer.writerows(all_books)

        print("Done scraping asynchronously 🚀")

if __name__ == "__main__":
    asyncio.run(main())
