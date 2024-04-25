import base64

from fastapi import Depends, FastAPI, HTTPException, Request, Response, File, UploadFile
from sqlalchemy.orm import Session
import logging

from . import crud
from . import schemas
from .database import SessionLocal

app = FastAPI(debug=True)

logger = logging.getLogger(__name__)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    except HTTPException as exc:
        response = exc
    except Exception as e:
        logger.exception("Internal server error: %s", e)
        response = Response("Internal server error", status_code=500)
    finally:
        request.state.db.close()
        return response


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students/", response_model=str)
async def create_student(
        student: schemas.StudentCreate,
        db: Session = Depends(get_db),):
    if crud.create_student(db, student):
        return "Student created successfully"
    logger.exception("Error in create_student endpoint: %s")
    raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/students/{student_id}/photo", response_model=str)
async def upload_photo(student_id: int, photo: UploadFile = File(...), db: Session = Depends(get_db)):
    if crud.upload_photo(db, student_id, photo.file.read()):
        return "Photo uploaded successfully"
    raise HTTPException(status_code=404, detail="Student not found")


@app.get("/students/", response_model=list[schemas.Student])
async def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        students = crud.get_students(db, skip=skip, limit=limit)
        for student in students:
            student.photo = base64.b64encode(student.photo).decode("utf-8")
        return students
    except Exception as e:
        logger.exception("Error while retrieving students: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/students/{student_id}", response_model=schemas.Student)
async def read_student(student_id: int, db: Session = Depends(get_db)):
    try:
        db_student = crud.get_student(db, student_id)
        if db_student is None:
            return HTTPException(status_code=404, detail="Student not found")
        db_student.photo = base64.b64encode(db_student.photo).decode("utf-8")
        return db_student
    except Exception as e:
        logger.exception("Error while retrieving student: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/students/{student_id}", response_model=str)
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    if crud.delete_student(db, student_id):
        return "Deleted successfully"
    raise HTTPException(status_code=404, detail="Student not found")
