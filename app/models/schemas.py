from pydantic import BaseModel
from datetime import date


class StudentBase(BaseModel):
    name: str
    date_of_birth: date
    photo: bytes
    grade: int
    student_group: str


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    student_id: int

    class Config:
        orm_mode = True
