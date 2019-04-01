from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://root:19918858@localhost:3306/sgh_users')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__='sgh_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False)
    realname=Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)
    email = Column(String(32), nullable=False)

class Content(Base):
    __tablename__='sgh_contents'
    id = Column(Integer, primary_key=True, autoincrement=False)
    text=Column(String(2048), nullable=False)

# class Database(Base):
#     __tablename__='sgh_datas'
#     id = Column(Integer, primary_key=True, autoincrement=False)
#     date_time=Column(String(32), nullable=False)
#     co2 = Column(String(32), nullable=False)
#     air_temp = Column(String(32), nullable=False)
#     air_humidity = Column(String(32), nullable=False)
#     illuminate = Column(String(32), nullable=False)
#     soil_temp = Column(String(32), nullable=False)
#     soil_humidity = Column(String(32), nullable=False)

def init():
    Base.metadata.create_all(engine)

# if __name__ == '__main__':
#     session=Session()
#     str=session.query(Content).filter(Content.id==1).one()
#     print(str.text)