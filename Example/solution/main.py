from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from databases.crud import *
from databases.shemas import *
from databases.db import *

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/tags/", response_model=List[Tag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = get_tags(db, skip=skip, limit=limit)
    return tags


@app.get("/tags/{tag_id}", response_model=Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = get_tag(db, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@app.post("/tags/", response_model=Tag)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    return create_tag_crud(db=db, tag=tag)


@app.put("/tags/{tag_id}", response_model=Tag)
def update_tag(tag: TagUpdate, tag_id: int, db: Session = Depends(get_db)):
    tag = update_tag_crud(db, tag_id, tag)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@app.delete("/tags/{tag_id}", response_model=Tag)
def remove_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = remove_tag_crud(db, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@app.get("/notes/", response_model=List[Note])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = get_notes(db, skip=skip, limit=limit)
    return tags


@app.get("/notes/{note_id}", response_model=Note)
def read_note(note_id: int, db: Session = Depends(get_db)):
    note = get_note(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.post("/notes/", response_model=Note)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return create_note_crud(db=db, note=note)


@app.delete("/notes/{note_id}", response_model=Note)
def remove_note(note_id: int, db: Session = Depends(get_db)):
    note = remove_note_crud(db, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.patch("/notes/{note_id}", response_model=Note)
def done_note(note: NoteDone, note_id: int, db: Session = Depends(get_db)):
    note = done_note_crud(db, note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
