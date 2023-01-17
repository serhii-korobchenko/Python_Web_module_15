
from sqlalchemy.orm import Session, subqueryload
from .models  import Alarm, News
from .shemas import AlarmUpdate, NewsUpdate

def get_alarms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Alarm).offset(skip).limit(limit).all()


def get_alarm(db: Session, alarm_id: int):
    return db.query(Alarm).filter(Alarm.id == alarm_id).first()



def update_alarm_crud(db: Session, alarm_id: int, alarm: AlarmUpdate):
    db_alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()
    if db_alarm:
        db_alarm.name = alarm.name
        db_alarm.start_time = alarm.start_time
        db_alarm.finish_time = alarm.finish_time
        db.commit()
    return db_alarm


def remove_alarm_crud(db: Session, alarm_id: int):
    db_alarm = db.query(Alarm).filter(Alarm.id == alarm_id).first()
    if db_alarm:
        db.delete(db_alarm)
        db.commit()
    return db_alarm

def get_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(News).offset(skip).limit(limit).all()


def get_one_news(db: Session, news_id: int):
    return db.query(News).filter(News.id == news_id).first()


def update_news_crud(db: Session, news_id: int, news: NewsUpdate):
    db_news = db.query(News).filter(News.id == news_id).first()
    if db_news:
        db_news.news_content = news.news_content
        db_news.news_time = news.news_time
        db.commit()
    return db_news


def remove_news_crud(db: Session, news_id: int):
    db_news = db.query(News).filter(News.id == news_id).first()
    if db_news:
        db.delete(db_news)
        db.commit()
    return db_news

def get_events(db: Session):
    return db.query(Alarm).filter(Alarm.news != None).all()