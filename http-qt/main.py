from fastapi import Depends, FastAPI, HTTPException, Request, Response, File
from sqlalchemy.orm import Session
import logging

from . import crud
from . import schemas
from .database import SessionLocal

app = FastAPI(debug=True)

logger = logging.getLogger(__name__)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    except HTTPException as exc:
        response = exc
    finally:
        request.state.db.close()
        return response


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students/", response_model=schemas.Student)
async def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    try:
        db_student = crud.create_student(db, student)
        return db_student
    except Exception as exc:
        logger.exception("Error in create_student endpoint: %s", str(exc))
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/students/{student_id}/photo", response_model=str)
async def upload_photo(student_id: int, photo: bytes = File(...), db: Session = Depends(get_db)):
    if crud.upload_photo(db, student_id, photo):
        return "Photo uploaded successfully"
    raise HTTPException(status_code=404, detail="Student not found")


@app.get("/students/", response_model=list[schemas.Student])
async def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students


@app.get("/students/{student_id}", response_model=schemas.Student)
async def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id)
    if db_student is None:
        return HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.delete("/students/{student_id}", response_model=str)
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    if crud.delete_student(db, student_id):
        return "Deleted successfully"
    raise HTTPException(status_code=404, detail="Student not found")
