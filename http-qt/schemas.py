from typing import Optional

from pydantic import BaseModel
from datetime import date


class StudentBase(BaseModel):
    name: str
    date_of_birth: date
    photo: Optional[str]
    grade: int
    student_group: str


class StudentCreate(BaseModel):
    name: str
    date_of_birth: str
    grade: int
    student_group: str
    photo: Optional[bytes]

    class Config:
        orm_mode = True


class Student(StudentBase):
    id: int


class Config:
    orm_mode = True
