# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY book_api/ ./book_api
COPY books_with_country.json ./book_api/books_with_country.json

# Install requirements
RUN pip install --no-cache-dir -r book_api/requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "book_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
