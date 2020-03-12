from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary, UnicodeText, MetaData)

CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8".format(
    drivername="mysql",
    user="root",
    passwd="oberyn martel",
    host="localhost",
    port="3306",
    db_name="dataak_forum_pure",
)

DeclarativeBase = declarative_base()


# database models for the respective tables
class Forums(DeclarativeBase):
    """
    Database model for Forums table
    """
    __tablename__ = 'forums'
    id = Column(Integer, primary_key=True)
    forum_name = Column(Text)
    url = Column(Text)


class Threads(DeclarativeBase):
    """
    Database model for Threads table
    """
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    forum_id = Column(Integer, ForeignKey('forums.id'))

    thread = Column(Text)
    url = Column(Text)


class Authors(DeclarativeBase):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(Text)


class Posts(DeclarativeBase):
    """
    Database model for Posts table
    """
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey('threads.id'))
    author_id = Column(Integer, ForeignKey('authors.id'))
    body = Column(Text)
