from sqlalchemy import Column,Integer,Float,String,DATE
from databases import Base

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
    enrollment_date = Column(DATE)