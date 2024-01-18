from fastapi import APIRouter
from app.crud import crud
from ..models.schemas import Student, StudentCreate, StudentUpdate

router = APIRouter()


@router.get("/students/{student_id}", response_model=Student)
async def read_student(student_id: int):
    return await crud.get_student(student_id)


@router.get("/students/", response_model=list[Student])
async def read_students(skip: int = 0, limit: int = 10):
    return await crud.get_students(skip=skip, limit=limit)


@router.post("/students/", response_model=Student)
async def create_student(student: StudentCreate):
    # Read the content of the uploaded file
    photo_content = await student.photo.read()
    student_dict = student.dict(exclude={'photo'})
    student_id = await crud.create_student(student_dict, photo_content)
    return {"student_id": student_id, **student.dict()}


@router.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: int, student: StudentUpdate):
    # Read the content of the uploaded file
    photo_content = await student.photo.read()
    student_dict = student.dict(exclude={'photo'})
    return await crud.update_student(student_id, student_dict, photo_content)


@router.delete("/students/{student_id}", response_model=int)
async def delete_student_api(student_id: int):
    return await crud.delete_student(student_id)
