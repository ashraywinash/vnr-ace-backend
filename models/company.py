from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.db import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    sector = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
