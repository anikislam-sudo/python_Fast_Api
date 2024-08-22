from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import Course, CourseCreate, Enrollment, EnrollmentCreate
from .services import CourseService, EnrollmentService
from .databases import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_enrollment_service(db: Session = Depends(get_db)):
    return EnrollmentService(db)

@router.get("/courses", response_model=list[Course])
def read_courses(db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.get_courses()

@router.post("/courses", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    service = CourseService(db)
    return service.create_course(
        title=course.title,
        description=course.description,
        instructor=course.instructor,
        duration=course.duration,
        price=course.price
    )

@router.get("/courses/{course_id}", response_model=Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    service = CourseService(db)
    course = service.get_course_by_id(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/enrollments", response_model=Enrollment)
def enroll_student(enrollment: EnrollmentCreate, service: EnrollmentService = Depends(get_enrollment_service)):
    # Pass both `student_name` and `course_id` to `validate_enrollment`
    if not service.validate_enrollment(enrollment.student_name, enrollment.course_id):
        raise HTTPException(status_code=400, detail="Invalid enrollment or student already enrolled")
    
    # Proceed with enrollment
    return service.enroll_student(
        student_name=enrollment.student_name, 
        course_id=enrollment.course_id
    )
