from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite', echo=False)
Session = sessionmaker(bind=engine)

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    usage = relationship("UsageEntry", back_populates="device")

class UsageEntry(Base):
    __tablename__ = 'usage_entries'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    app_name = Column(String)
    seconds = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    background = Column(Boolean, default=False)
    device = relationship("Device", back_populates="usage")

def init_db():
    Base.metadata.create_all(engine)