from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from databases.crud import *
from databases.shemas import *
from databases.db import *

app = FastAPI()


@app.get("/")
async def news_correlated_to_air_raid_alarms_in_kyiv():
    return {"message": "Welcome to Kyiv news database! Content: News correlated to Air raid Alarms in Kyiv"}


@app.get("/alarms/", response_model=List[Alarm])
def read_alarms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alarms = get_alarms(db, skip=skip, limit=limit)
    return alarms


@app.get("/alarms/{alarm_id}", response_model=Alarm)
def read_alarm(alarm_id: int, db: Session = Depends(get_db)):
    alarm = get_alarm(db, alarm_id)
    if alarm is None:
        raise HTTPException(status_code=404, detail="Alarm not found")
    return alarm


@app.put("/alrms/{alarm_id}", response_model=Alarm)
def update_alarm(alarm: AlarmUpdate, alarm_id: int, db: Session = Depends(get_db)):
    alarm = update_alarm_crud(db, alarm_id, alarm)
    if alarm is None:
        raise HTTPException(status_code=404, detail="Alarm not found")
    return alarm


@app.delete("/alarms/{alarm_id}", response_model=Alarm)
def remove_alarm(alarm_id: int, db: Session = Depends(get_db)):
    alarm = remove_alarm_crud(db, alarm_id)
    if alarm is None:
        raise HTTPException(status_code=404, detail="Alarm not found")
    return alarm


@app.get("/news/", response_model=List[News])
def read_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    news = get_news(db, skip=skip, limit=limit)
    return news


@app.get("/news/{news_id}", response_model=News)
def read_specific_news(news_id: int, db: Session = Depends(get_db)):
    news = get_one_news(db, news_id)
    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@app.put("/news/{news_id}", response_model=News)
def update_news(news: NewsUpdate, news_id: int, db: Session = Depends(get_db)):
    news = update_news_crud(db, news_id, news)
    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return news



@app.delete("/news/{news_id}", response_model=News)
def remove_news(news_id: int, db: Session = Depends(get_db)):
    news = remove_news_crud(db, news_id)
    if news is None:
        raise HTTPException(status_code=404, detail="News not found")
    return news


@app.get("/events/", response_model=List[Alarm])
def read_events_during_alarms(db: Session = Depends(get_db)):
    events = get_events(db)
    return events
