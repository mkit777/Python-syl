from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer,DateTime

Base = declarative_base()
engine = create_engine('mysql://root@localhost:3306/shiyanlougithub?charset=utf8')


class Repositories(Base):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    update_time = Column(DateTime)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
