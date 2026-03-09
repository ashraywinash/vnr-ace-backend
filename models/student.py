from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from core.db import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    roll_no = Column(String, unique=True, index=True, nullable=False)
    
    full_name = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    dob = Column(String, nullable=True) # Or Date depending on exact need
    branch = Column(String, index=True, nullable=True)
    email = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    
    cgpa = Column(Float, nullable=True)
    tenth_cgpa = Column(Float, nullable=True)
    inter_percent = Column(Float, nullable=True)
    active_backlogs = Column(Integer, nullable=True, default=0)
    passive_backlogs = Column(Integer, nullable=True, default=0)
    
    category = Column(String, nullable=True)
    home_town = Column(String, nullable=True)
    district = Column(String, nullable=True)
    state = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    
    minor_degree = Column(String, nullable=True)
    intern_status = Column(Boolean, nullable=True, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
