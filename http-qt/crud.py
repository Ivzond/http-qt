from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from . import models, schemas
import logging

logger = logging.getLogger(__name__)


def get_student(db: Session, student_id: int):
    try:
        student = db.query(models.Student).filter(models.Student.id == student_id).first()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except Exception as e:
        logger.exception("Error while retrieving student: %s", e)
        raise


def get_students(db: Session, skip: int = 0, limit: int = 100):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return True


def upload_photo(db: Session, student_id: int, photo_content: bytes):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.photo = photo_content
    db.commit()
    db.refresh(db_student)
    return True


def delete_student(db: Session, student_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
        return True
    return False
