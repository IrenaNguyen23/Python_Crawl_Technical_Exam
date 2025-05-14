# 📚 Web Scrape Books API Project

A Python project that scrapes book data from the web, enriches it with country metadata, and exposes a RESTful API to interact with the data.

---

## 🚀 Requirements

- Python 3.10+
- `pip`
- Docker (optional)
- Docker Compose (optional)
- Git

---

## 🧰 Setup Instructions

### 1. Clone the Repository

  ```
  git clone https://github.com/IrenaNguyen23/Python_Crawl_Technical_Exam.git
  cd Python_Crawl_Technical_Exam
  ```

### 2. Run Locally with Virtual Environment
  ```
  python3 -m venv venv
  source venv/bin/activate     # Linux/Mac
  venv\Scripts\activate        # Windows

  pip install -r book_api/requirements.txt

  uvicorn book_api.main:app --reload
  ➡️ The API will be available at: http://127.0.0.1:8000
  ```

3. Run with Docker
Option A: Docker
```
docker build -t webscrape-books .
docker run -p 8000:8000 webscrape-books
```

Option B: Docker Compose (Recommended ✅)
```
docker-compose up --build
➡️ Open: http://localhost:8000/docs
```

✅ API Endpoints
Method	Endpoint	Description
GET	/books	Retrieve all books
GET	/books?country=XX	Filter books by publisher country
POST	/books	Add a new book (requires API key)
DELETE	/books/{title}	Delete a book by title (requires API key)

🔐 API Key Header (for POST/DELETE):
X-API-Key: supersecretkey
🧪 Run Unit Tests
```
pytest tests/
```
Output Files (Included)
books.csv – Raw scraped book data

books_with_country.csv / .json – Data enriched with publisher country

html_backup/ – Folder of raw HTML files from scraping step

Dockerized Components
Dockerfile – Defines containerized FastAPI app

docker-compose.yml – One-command setup for API
📝 Notes
All scraped/enriched data is loaded on API startup from book_api/books_with_country.json.

Adding/deleting books will update this file automatically.


Made with ☕ & 💻 by @IrenaNguyen23
