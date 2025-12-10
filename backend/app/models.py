from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class CheckRecord(Base):
    __tablename__ = "checks"

    id = Column(String, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    status = Column(String, default="ANALYSING")
    result = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
