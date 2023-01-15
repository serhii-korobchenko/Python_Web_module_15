from sqlalchemy import create_engine, Column, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings
from datetime import datetime
from sqlalchemy.sql.schema import ForeignKey, Table

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)



# Association Table for Many-to-Many relationship between Alarm and News
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
alarm_news = Table('alarm_news', Base.metadata,
    Column("id", Integer, primary_key=True),
    Column('alarm_id', Integer, ForeignKey('alarm.id')),
    Column('news_id', Integer, ForeignKey('news.id'))
                   )




class Alarm(Base):
    __tablename__ = "alarm"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=False)
    start_time = Column('start_time', DateTime, default=datetime.now())
    finish_time = Column('finish_time',DateTime, default=datetime.now())
    news = relationship("News", secondary = alarm_news, backref="alarm")



class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    news_content = Column('news_content', Text())
    news_time = Column('news_time', DateTime, default=datetime.now())
    ref = Column('ref', String(200), unique=False)
    #alarms = relationship("Alarm", secondary=alarm_news, backref="news")




