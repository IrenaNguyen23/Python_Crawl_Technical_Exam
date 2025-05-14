# Web Scrape Books API Project

## Requirements
- Python 3.10+
- Docker (optional)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/webscrape_books.git
   cd webscrape_books

2. **Create a Virtual Environment**:
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate  # Windows
3. **Install Dependencies**:

    pip install -r book_api/requirements.txt
4. **Run the API Locally**:

    Without Docker:

    uvicorn book_api.main:app --reload
    The API will be available at http://127.0.0.1:8000.

    With Docker:

    docker build -t webscrape-books .
    docker run -p 8000:8000 webscrape-books
5. **Testing**:

    To run unit tests:

    pytest tests/
6.   **API Endpoints**:

GET /books: Retrieve all books.

GET /books?country=<country_name>: Retrieve books by publisher country.

POST /books: Add a new book to the list.

DELETE /books/{title}: Delete a book by title.