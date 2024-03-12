import base64

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from . import models, schemas


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


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
