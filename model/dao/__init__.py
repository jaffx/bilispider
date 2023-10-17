import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_, not_
from sqlalchemy import Integer, String, Column, DateTime,BigInteger
from libs.init import *

engine = sqlalchemy.create_engine("mysql+pymysql://root:@localhost:3306/xbili")


class DaoBase:
    smaker = sessionmaker(bind=engine)
    logger = logging.getLogger("DB")

    def __init__(self):
        self.session = self.smaker()

    def add(self, instance, commit=True) -> (int | None):
        try:
            self.session.add(instance)
            self.session.flush()
            _id = instance.id
            if commit:
                self.session.commit()
        except Exception as e:
            self.logger.error(f"Dao add instance failed for {e}")
            return None
        else:
            return _id

    def add_all(self, instances: list) -> int:
        succ = 0
        for instance in instances:
            if self.add(instance, commit=False):
                succ += 1
        if succ > 0:
            self.session.commit()
        return succ



fileHandler = logging.FileHandler("./log/db.log")
fileHandler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
fileHandler.setLevel(logging.WARNING)
DaoBase.logger.addHandler(fileHandler)
