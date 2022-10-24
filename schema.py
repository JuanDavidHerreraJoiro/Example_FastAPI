from pydantic import BaseModel
from typing import List, Optional

class Author(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

    class Config:
        orm_mode = True

class Book(BaseModel):
    title: Optional[str] = None
    rating: Optional[int] = None
    author_id: Optional[int] = None
    author: Optional[Author]

    class Config:
        orm_mode = True
