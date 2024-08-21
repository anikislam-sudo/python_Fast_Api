from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from .databases import SessionLocal
from .services  import CourseService,EnrollmentService
from .schemas import  Course,CourseCreate,Enrollment,EnrollmentCreate


router=APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/courses",response_model=list[Course])       

def read_courses(db: Session = Depends(get_db)):
    service=CourseService(db)
    return service.get_courses()

@router.post("/courses",response_model=Course)

def create_course(course:CourseCreate,db:Session=Depends(get_db)):
    service=CourseService(db)
    return service.create_course(
        title=course.title,
        description=course.description,
        instructor=course.instructor,
        duration=course.duration,
        price=course.price


    )

@router.get("/courses/{course_id}",response_model=Course)
def read_course(course_id=int,db:Session=Depends(get_db)):
    service = CourseService(db)
    course = service.get_course_by_id(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/enrollments", response_model=Enrollment)
def create_enrollment(enrollment:EnrollmentCreate,db:Session=Depends(get_db)):
    service = EnrollmentService(db)
    if not service.validate_enrollment(enrollment.student_name, enrollment.course_id):
        raise HTTPException(status_code=400, detail="Invalid enrollment")
    return service.enroll_student(
        student_name=enrollment.student_name,
        course_id=enrollment.course_id,
        enrollment_date=enrollment.enrollment_date
    )
