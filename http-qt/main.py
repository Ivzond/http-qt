from fastapi import FastAPI, Depends, Body, HTTPException
from .database import get_db, engine, Student
from .models import StudentCreate
from sqlalchemy.orm import Session

app = FastAPI()


@app.post("/students")
async def create_student(
        student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        name=student.name,
        date_of_birth=student.date_of_birth,
        photo=student.photo,
        grade=student.grade,
        student_group=student.student_group,
    )
    db.add(new_student)
    db.commit()
    return new_student


@app.get("/students/{student_id}")
async def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.delete("/students/{student_id")
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    db.query(Student).filter(Student.id == student_id).delete()
    db.commit()
    return {"message": "Student deleted successfully"}
