from sqlalchemy import crate_engine
from sqlalchemy.ext.declaractive import declaractive_base
from sqlalchemy import Column, String, Integer,DateTime

Base = declaractive_base()
engine = crate_engine('mysql://root@localhost:3306/shiyanlou?charset=utf8')


class Repositories(Base):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_Key=True)
    name = Column(String(64))
    update_time = Column(DateTime)
