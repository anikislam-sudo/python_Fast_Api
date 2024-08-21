from pydantic import BaseModel
from typing  import Optional


class CourseBase (BaseModel):
    title: str
    description: str
    instructor: str
    duration: int
    price: float

class CourseCreate(CourseBase):
    pass
class Course(CourseBase):
    id:int
   
class Config:
    orm_mode=True

class EnrollmentBase (BaseModel):
    student_name:str
    course_id:int
    enrollment_date:str

class EnrollmentCreate(EnrollmentBase):
    pass 

class Enrollment (EnrollmentBase):
    id:int

class Config:
    orm_mode=True    