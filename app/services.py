from sqlalchemy.orm import Session
from datetime import datetime
from .models import Course, Enrollment

class CourseService:
    def __init__(self, db: Session):
        self.db = db

    def get_courses(self):
        return self.db.query(Course).all()

    def create_course(self, title: str, description: str, instructor: str, duration: int, price: float):
        db_course = Course(title=title, description=description, instructor=instructor, duration=duration, price=price)
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course

    def get_course_by_id(self, course_id: int):
        return self.db.query(Course).filter(Course.id == course_id).first()

    def filter_courses(self, instructor: str = None, price: float = None, duration: int = None):
        query = self.db.query(Course)
        if instructor:
            query = query.filter(Course.instructor == instructor)
        if price:
            query = query.filter(Course.price <= price)
        if duration:
            query = query.filter(Course.duration <= duration)
        return query.all()

class EnrollmentService:
    def __init__(self, db: Session):
        self.db = db

    def enroll_student(self, student_name: str, course_id: int):
        # Automatically set the enrollment date to the current date
        enrollment_date = datetime.utcnow()
        db_enrollment = Enrollment(student_name=student_name, course_id=course_id, enrollment_date=enrollment_date)
        self.db.add(db_enrollment)
        self.db.commit()
        self.db.refresh(db_enrollment)
        return db_enrollment

    def validate_enrollment(self, student_name: str, course_id: int):
        # Check if the course exists
        course = self.db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return False
        # Check if the student is already enrolled in the course
        existing_enrollment = self.db.query(Enrollment).filter(
            Enrollment.student_name == student_name,
            Enrollment.course_id == course_id
        ).first()
        if existing_enrollment:
            return False
        return True
