from sqlalchemy.dialects.mysql.types import DATETIME, DOUBLE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Unicode
from sqlalchemy.dialects.mysql import INTEGER
from passlib.hash import pbkdf2_sha256
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.schema import ForeignKey
import datetime

from sqlalchemy.sql.sqltypes import String
Base = declarative_base()
metadata = Base.metadata


class Persons(Base):
    __tablename__ = 'Persons'
    id = Column(INTEGER(), primary_key=True)
    username = Column(String(100), nullable=False)
    surname  = Column(String(100), nullable=False)
    password = Column(String(250), nullable=False)
    token =  Column(String(250), nullable=True)
    def verify_password(self, raw_password):
        return pbkdf2_sha256.verify(raw_password, self.password)

    @staticmethod
    def hash_password(raw_password):
        return pbkdf2_sha256.hash(raw_password)


class ServiceLog(Base):
    __tablename__ = 'servicelogs'

    id = Column(INTEGER(), primary_key=True)
    user_id = Column(None, ForeignKey('Persons.id'), nullable=True)
    ip_address = Column(Unicode(15), nullable=False)
    request_time = Column(DATETIME(), default=datetime.datetime.now)

class Event(Base):
    __tablename__ = 'Event'

    id = Column(INTEGER(), primary_key=True)
    title = Column(String(100), nullable=False)
    description   = Column(String(100), nullable=False)
    price = Column(DOUBLE(18,2), nullable=False)
    date = Column(DATETIME(), default=datetime.datetime.now)

class Coupon(Base):
    __tablename__ = 'Coupon'
    id = Column(INTEGER(), primary_key=True)
    event_id = Column(None, ForeignKey('Event.id'), nullable=False)
    user_id = Column(None, ForeignKey('Persons.id'), nullable=False)
    hash =  Column(String(250), nullable=False)
    comments = Column(String(250), nullable=True)