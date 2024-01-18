from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Student
from ..crud import get_students, get_student, create_student, update_student, delete_student

router = APIRouter()


@router.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/students/")
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = get_students(db, skip=skip, limit=limit)
    return students


@router.post("/students/")
def create_student_api(student: Student, db: Session = Depends(get_db)):
    return create_student(db, student)


@router.put("/students/{student_id}")
def update_student_api(student_id: int, updated_data: dict, db: Session = Depends(get_db)):
    return update_student(db, student_id, updated_data)


@router.delete("/students/{student_id}")
def delete_student_api(student_id: int, db: Session = Depends(get_db)):
    return delete_student(db, student_id)
