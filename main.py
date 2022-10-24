import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import Author
from models import Author as ModelAuthor
from models import Book
from models import Book as ModelBook
from schema import Author as SchemaAuthor
from schema import Book as SchemaBook

load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/books/")
# def get_books():
#     books = db.session.query(Book).all()
#     return books

@app.post("/add-book/", response_model=SchemaBook)
def add_book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book


@app.post("/add-author/", response_model=SchemaAuthor)
def add_author(author: SchemaAuthor):
    db_author = ModelAuthor(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author

@app.get("/books/")
def get_books():
    books = db.session.query(Book, Author).join(Book, Author.id == Book.author_id).all()

    return books

@app.get("/authors/")
def get_authors():
    authors = db.session.query(Author).all()

    return authors

@app.get("/book/{book_id}")
def get_book(book_id: int):
    book = db.session.query(Book, Author).filter(Book.id == book_id).\
            join(Book, Author.id == Book.author_id).all()

    return book

@app.get("/author/{author_id}")
def get_author(author_id: int):
    author = db.session.query(Author).filter(Author.id == author_id).all()
    
    return author

#No elimina si el autor ya pertenece a un libro registrado en la db
@app.delete("/delete_author/{author_id}")
def delete_author(author_id: int):
    author = db.session.query(Author).filter(Author.id == author_id).first()
    db.session.delete(author)
    db.session.commit()

    return "Eliminado"
#
@app.delete("/delete_book/{book_id}")
def delete_book(book_id: int):
    book = db.session.query(Book).filter(Book.id == book_id).first()
    db.session.delete(book)
    db.session.commit()

    return "Eliminado"

@app.put("/update_author/{author_id}", response_model=SchemaAuthor)
def update_author(author_id: int, author_new: SchemaAuthor):
    author_old = db.session.query(Author).filter(Author.id == author_id).first()
    
    author_old.name = author_new.name
    author_old.age = author_new.age

    db.session.commit()
    db.session.refresh(author_old)
    
    return author_old

@app.put("/update_book/{book_id}", response_model=SchemaBook)
def update_book(book_id: int, book_new: SchemaBook):
    book_old = db.session.query(Book).filter(Book.id == book_id).first()
    
    book_old.title = book_new.title
    book_old.rating = book_new.rating
    book_old.author_id = book_new.author_id

    db.session.commit()
    db.session.refresh(book_old)
    
    return book_old

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
