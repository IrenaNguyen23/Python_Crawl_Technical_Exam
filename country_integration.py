import requests
import csv
import json
import random


def get_all_countries():
    url = "https://restcountries.com/v3.1/all"
    resp = requests.get(url)
    resp.raise_for_status()
    countries_data = resp.json()
    country_names = [c["name"]["common"] for c in countries_data]
    print(f"Fetched {len(country_names)} countries.")
    return country_names


def load_books_from_csv(file_path):
    books = []
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append(row)
    print(f"Loaded {len(books)} books from {file_path}")
    return books


def assign_random_countries(books, country_list):
    for book in books:
        book["publisher_country"] = random.choice(country_list)
    return books


def save_to_csv(books, file_path):
    fieldnames = list(books[0].keys())
    with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)
    print(f"Saved CSV to {file_path}")


def save_to_json(books, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON to {file_path}")


def main():
    books = load_books_from_csv("books.csv")  
    countries = get_all_countries()
    books_with_country = assign_random_countries(books, countries)

    save_to_csv(books_with_country, "books_with_country.csv")
    save_to_json(books_with_country, "books_with_country.json")
    print("🎉 Done! Book data now includes publisher countries.")


if __name__ == "__main__":
    main()
