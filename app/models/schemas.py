from sqlalchemy import Column, Integer, String, Date, BINARY
from sqlalchemy.ext.declarative import declarative_base
from fastapi import UploadFile
from pydantic import BaseModel
from datetime import date

Base = declarative_base()


class StudentBase(BaseModel):
    name: str
    date_of_birth: date
    grade: int
    student_group: str


class StudentCreate(StudentBase):
    name: str
    date_of_birth: date
    grade: int
    student_group: str
    photo: UploadFile


class StudentUpdate(StudentBase):
    photo: UploadFile


class Student(StudentBase):
    student_id: int

    class Config:
        orm_mode = True


class StudentDB(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date_of_birth = Column(Date)
    photo = Column(BINARY)
    grade = Column(Integer)
    student_group = Column(String)
