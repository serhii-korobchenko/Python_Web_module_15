
from sqlalchemy.orm import Session, subqueryload
from .models  import Alarm, News
# from .shemas import TagCreate, TagUpdate, NoteCreate, NoteDone




def get_alarms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Alarm).offset(skip).limit(limit).all()


# def get_tag(db: Session, tag_id: int):
#     return db.query(Tag).filter(Tag.id == tag_id).first()
#
#
# def create_tag_crud(db: Session, tag: TagCreate):
#     db_tag = Tag(name=tag.name)
#     db.add(db_tag)
#     db.commit()
#     db.refresh(db_tag)
#     return db_tag
#
#
# def update_tag_crud(db: Session, tag_id: int, tag: TagUpdate):
#     db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
#     if db_tag:
#         db_tag .name = tag.name
#         db.commit()
#     return db_tag
#
#
# def remove_tag_crud(db: Session, tag_id: int):
#     db_tag = db.query(Tag)\
#         .filter(Tag.id == tag_id)\
#         .first()
#     if db_tag:
#         db.delete(db_tag)
#         db.commit()
#     return db_tag

def get_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(News).offset(skip).limit(limit).all()


# def get_note(db: Session, note_id: int):
#     return db.query(Note).filter(Note.id == note_id).first()
#
#
# def create_note_crud(db: Session, note: NoteCreate):
#     tags = db.query(Tag).filter(Tag.id.in_(note.tags)).all()
#     db_note = Note(name=note.name, description=note.description, tags=tags)
#     db.add(db_note)
#     db.commit()
#     db.refresh(db_note)
#     return db_note
#
#
# def remove_note_crud(db: Session, note_id: int):
#     db_note = db.query(Note)\
#         .options(subqueryload(Note.tags))\
#         .filter(Note.id == note_id)\
#         .first()
#     if db_note:
#         db.delete(db_note)
#         db.commit()
#     return db_note
#
#
# def done_note_crud(db: Session, note: NoteDone, note_id: int):
#     db_note = db.query(Note).filter(Note.id == note_id).first()
#     if db_note:
#         db_note.done = note.done
#         db.commit()
#     return db_note