# app/models.py
from sqlalchemy import Column, Integer, String, Float,Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    instructor = Column(String)
    duration = Column(Integer)
    price = Column(Float)

class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    course_id = Column(Integer)
    enrollment_date = Column(Date)
