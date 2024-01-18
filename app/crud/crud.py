from sqlalchemy import select, update, delete

from ..db.database import database
from ..models.schemas import StudentDB


async def get_student(student_id: int):
    query = select(StudentDB).where(StudentDB.student_id == student_id)
    return await database.fetch_one(query)


async def get_students(skip: int = 0, limit: int = 10):
    query = select(StudentDB).offset(skip).limit(limit)
    return await database.fetch_all(query)


async def create_student(student: dict, photo_content: bytes):
    query = StudentDB.__tablename__.insert().values(**student, photo=photo_content)
    student_id = await database.execute(query)
    return student_id


async def update_student(student_id: int, student: dict, photo_content: bytes):
    query = (
        update(StudentDB)
        .where(StudentDB.student_id == student_id)
        .values(**student, photo=photo_content)
    )
    return await database.execute(query)


async def delete_student(student_id: int):
    query = delete(StudentDB).where(StudentDB.student_id == student_id)
    return await database.execute(query)
