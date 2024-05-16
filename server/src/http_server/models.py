from sqlalchemy import Column, Integer, String, LargeBinary, Date
from server.src.http_server.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    date_of_birth = Column(Date)
    photo = Column(LargeBinary)
    grade = Column(Integer)
    student_group = Column(String)
