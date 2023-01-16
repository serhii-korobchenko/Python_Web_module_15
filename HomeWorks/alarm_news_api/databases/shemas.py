from datetime import datetime
from typing import List
from pydantic import BaseModel


class NewsBase(BaseModel):
    news_content: str



# class NewsCreate(NewsBase):
#     tags: List[int]
#
#
# class NewsDone(BaseModel):
#     done: bool


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
# class AlarmUpdate(AlarmBase):
#     pass


class Alarm(AlarmBase):
    id: int
    start_time: datetime
    finish_time: datetime
    news: List[News]

    class Config:
        orm_mode = True


