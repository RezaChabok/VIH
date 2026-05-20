from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

Base = declarative_base()

class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    text = Column(String)

class Post(Base):
    __tablename__ = 'posts'
    link = Column(String, primary_key=True)
    title = Column(String)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
