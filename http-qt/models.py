from pydantic import BaseModel
from datetime import date


class StudentCreate(BaseModel):
    name: str
    date_of_birth: date
    photo: bytes
    grade: int
    student_group: str
