from fastapi import FastAPI, HTTPException
from typing import List
from models import Book
from schemas import BookCreate

app = FastAPI()

# In-memory database
books_db = []

@app.get("/books", response_model=List[Book])
def get_books():
    return books_db

@app.post("/books", response_model=Book)
def create_book(book: BookCreate):
    new_book = Book(id=len(books_db) + 1, **book.model_dump())
    books_db.append(new_book)
    return new_book


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate):
    for index, existing_book in enumerate(books_db):
        if existing_book.id == book_id:
            updated_book = Book(id=book_id, **book.model_dump())
            books_db[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db.pop(index)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
