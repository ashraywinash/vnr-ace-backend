from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from core.db import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    event_type = Column(String, index=True) # e.g., 'query', 'execution', 'error'
    user_id = Column(Integer, index=True, nullable=True)
    agent_name = Column(String, index=True)
    details = Column(JSON) # Store final_response, user_query, etc.
