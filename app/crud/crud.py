from sqlalchemy.orm import Session
from ..models import Student


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.student_id == student_id).first()


def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Student).offset(skip).limit(limit).all()


def create_student(db: Session, student: Student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, student_id: int, updated_data: dict):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student:
        for key, value in updated_data.items():
            setattr(student, key, value)
        db.commit()
        db.refresh(student)
    return student


def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student:
        db.delete(student)
        db.commit()
    return student
