from sqlalchemy import UUID, Column, String, Float, Integer, DateTime
from datetime import datetime
from .database import Base


class AlertModel(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID, unique=True, index=True)
    video = Column(String)
    store = Column(String)
    timestamp = Column(Float)
    resolution = Column(String)
    received_at = Column(DateTime, default=datetime.now())
