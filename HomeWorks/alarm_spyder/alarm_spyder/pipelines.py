# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from .models import db_connect, create_table, Alarm, News


class AlarmSpyderPipeline:
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

        alarm = Alarm()
        alarm.name = item["result"][0]
        alarm.start_time = item["result"][1]
        alarm.finish_time = item["result"][2]



        # check whether the alarm exists
        exist_alarm = session.query(Alarm).filter_by(name=alarm.name).first()
        try:
            if exist_alarm is None:  # the current author exists

                session.add(alarm)

            #print(f"--------->  {session.query(Author).filter_by(name=author.name).first().id}")
            quote.author_id = session.query(Author).filter_by(name=author.name).first().id
            session.add(quote)
            session.commit()


            for tag_item in item["keywords"]:
                exist_tag = session.query(Tag).filter_by(name=tag_item).first()
                if exist_tag is None:
                    tag = Tag()
                    tag.name = tag_item
                    tag.quote_id = session.query(Quote).filter_by(quote_content=quote.quote_content).first().id
                    session.add(tag)
                    session.commit()


        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

class SerhiiSpyderBotPipelineDetail:


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

        new_author = Author()
        new_author.name = item["author"][0]
        new_author.id = session.query(Author).filter_by(name=new_author.name).first().id
        new_author.ref = session.query(Author).filter_by(name=new_author.name).first().ref
        new_author.birthday = item["birthday"][0]
        new_author.bornlocation = item["bornlocation"][0]

        # check whether the author exists
        exist_author = session.query(Author).filter_by(name=new_author.name).first()
        try:
            if exist_author is not None:  # the current author exists

                session.delete(exist_author)
                session.commit()
                session.add(new_author)
                session.commit()


            #print(f"--------->  {session.query(Author).filter_by(name=author.name).first().id}")

            #session.commit()


        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item