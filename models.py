from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite', echo=False)
Session = sessionmaker(bind=engine)

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    usages = relationship("UsageEntry", back_populates="device")

class UsageEntry(Base):
    __tablename__ = 'usages'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    app_name = Column(String)
    seconds = Column(Integer)
    pickups = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    device = relationship("Device", back_populates="usages")

def init_db():
    Base.metadata.create_all(engine)
