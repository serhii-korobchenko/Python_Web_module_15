# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from .models import db_connect, create_table, Alarm, News, alarm_news
from datetime import datetime, timedelta
from sqlalchemy import and_, func

class AlarmSpyderPipeline:
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()

        alarm = Alarm()
        alarm.name = item["result"][0]
        alarm.start_time = datetime.strptime(item["result"][1], '%d.%m.%y %H:%M')
        alarm.finish_time = datetime.strptime(item["result"][2], '%d.%m.%y %H:%M')

        # check whether the alarm exists
        exist_alarm = session.query(Alarm).filter_by(name=alarm.name).first()
        query_news_ids = session.query(News).filter(and_(func.date(News.news_time) >= alarm.start_time),func.date(News.news_time) <= (alarm.finish_time+timedelta(hours=12))).all()

        print(f'query_news_ids -----> {query_news_ids}')

        try:
            if exist_alarm is None and query_news_ids is not None:  # the current alarm exists

                alarm.news = query_news_ids
                session.add(alarm)
                session.commit()

            #print(f"--------->  {session.query(Author).filter_by(name=author.name).first().id}")
            # quote.author_id = session.query(Author).filter_by(name=author.name).first().id
            # session.add(quote)
            # session.commit()

            # for tag_item in item["keywords"]:
            #     exist_tag = session.query(Tag).filter_by(name=tag_item).first()
            #     if exist_tag is None:
            #         tag = Tag()
            #         tag.name = tag_item
            #         tag.quote_id = session.query(Quote).filter_by(quote_content=quote.quote_content).first().id
            #         session.add(tag)
            #         session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

class NewsSpyderPipeline:


    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save quotes in the database
        This method is called for every item pipeline component
        """
        session = self.Session()

        # date reversing
        print(f'Date time------------->{"".join(item["date_time"])}')
        date_temp_list = "".join(item["date_time"]).split(', ')
        reversed_date = str(date_temp_list[1]) + " " + str(date_temp_list[0])
        print(f'Reversed date------------->{reversed_date}')
        print(f'news_content------------->{type(item["news_title"])}')
        print(f'news_ref------------->{type(item["news_ref"])}')

        news = News()
        news.news_content = "".join(item["news_title"])
        news.news_time = datetime.strptime(reversed_date, '%d.%m.%Y %H:%M')
        news.ref = "".join(item["news_ref"])


        # check whether the news exists
        exist_news = session.query(News).filter_by(ref=news.ref).first()
        #print(f'=============================> {exist_news}')
        try:
            if exist_news is None:  # the current author exists
                session.add(news)
                session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item