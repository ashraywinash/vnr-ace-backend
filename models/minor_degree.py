from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from core.db import Base

class MinorDegree(Base):
    __tablename__ = "minor_degrees"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    minor_name = Column(String, nullable=False)
    
    # Relationships
    student = relationship("Student")
