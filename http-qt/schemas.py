from pydantic import BaseModel
from datetime import date


class StudentBase(BaseModel):
    name: str
    date_of_birth: date
    photo: bytes
    grade: int
    student_group: str


class StudentCreate(BaseModel):
    name: str
    date_of_birth: date
    grade: int
    student_group: str

    class Config:
        orm_mode = True


class Student(StudentBase):
    id: int


class Config:
    orm_mode = True
