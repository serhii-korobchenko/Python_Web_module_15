from datetime import datetime
from typing import List
from pydantic import BaseModel


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


class NoteBase(BaseModel):
    name: str
    description: str


class NoteCreate(NoteBase):
    tags: List[int]


class NoteDone(BaseModel):
    done: bool


class Note(NoteBase):
    id: int
    created: datetime
    done: bool
    tags: List[Tag]

    class Config:
        orm_mode = True