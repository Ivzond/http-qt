from sqlalchemy import Column, Integer, String, LargeBinary, Date
from .database import Base


class Student(Base):
    tablename = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    date_of_birth = Column(Date)
    photo = Column(LargeBinary)
    grade = Column(Integer)
    student_group = Column(String)
