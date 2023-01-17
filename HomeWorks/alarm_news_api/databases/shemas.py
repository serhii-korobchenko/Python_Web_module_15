from datetime import datetime
from typing import List
from pydantic import BaseModel


class NewsBase(BaseModel):
    news_content: str



class NewsUpdate(NewsBase):
    news_time: datetime


class News(NewsBase):
    id: int
    news_time: datetime
    ref: str


    class Config:
        orm_mode = True

class AlarmBase(BaseModel):
    name: str


# class AlarmCreate(AlarmBase):
#     pass
#
#
class AlarmUpdate(AlarmBase):
    id: int
    start_time: datetime
    finish_time: datetime


class Alarm(AlarmBase):
    id: int
    start_time: datetime
    finish_time: datetime
    news: List[News]

    class Config:
        orm_mode = True


