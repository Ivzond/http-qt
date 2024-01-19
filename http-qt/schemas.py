from typing import Optional

from pydantic import BaseModel
from datetime import date


class StudentBase(BaseModel):
    name: str
    date_of_birth: date
    photo: Optional[str]
    grade: int
    student_group: str


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True
