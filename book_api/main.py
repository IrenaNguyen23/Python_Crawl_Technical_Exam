from fastapi import FastAPI, HTTPException, Query, Header, Depends
from typing import List, Optional
from pydantic import BaseModel
import json
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()


BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "books_with_country.json"

API_KEY = "supersecretkey"

books_data = []


class Book(BaseModel):
    title: str
    price: str
    availability: str
    product_page: str
    star_rating: int
    publisher_country: str

def authorize(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
@app.on_event("startup")
def load_books():
    global books_data
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            books_data = json.load(f)
    else:
        books_data = []


@app.get("/books", response_model=List[Book])
def get_books(country: Optional[str] = Query(None, description="Filter by country name")):
    if country:
        filtered = [book for book in books_data if book["publisher_country"].lower() == country.lower()]
        return filtered
    return books_data


@app.post("/books", response_model=Book)
def add_book(book: Book, _: str = Depends(authorize)):
    for b in books_data:
        if b["title"].lower() == book.title.lower():
            raise HTTPException(status_code=400, detail="Book already exists")
    books_data.append(book.dict())
    _save_data()
    logging.info(f"Adding book: {book.title}")
    return book


@app.delete("/books/{title}")
def delete_book(title: str, _: str = Depends(authorize)):
    global books_data
    original_len = len(books_data)
    books_data = [b for b in books_data if b["title"].lower() != title.lower()]
    if len(books_data) == original_len:
        raise HTTPException(status_code=404, detail="Book not found")
    _save_data()
    logging.info(f"Deleted book: {title}")
    return {"message": f"Deleted book: {title}"}

@app.get("/")
def root():
    return {"message": "Welcome to Book API 🧠📚. Go to /docs for Swagger UI."}


def _save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books_data, f, indent=2, ensure_ascii=False)
