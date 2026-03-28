from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from core.db import Base

class CompanyPrepQuestion(Base):
    __tablename__ = "company_prep_questions"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False, index=True)
    experiences = Column(JSONB, nullable=True)  # List of strings
    questions = Column(JSONB, nullable=True)    # List of strings
    created_at = Column(DateTime(timezone=True), server_default=func.now())
