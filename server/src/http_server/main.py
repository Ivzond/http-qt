import os
import base64
import configparser
import logging
from logging.config import fileConfig

from fastapi import Depends, FastAPI, HTTPException, Request, Response, File, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from server.src.http_server import crud, schemas
from server.src.http_server.database import SessionLocal

app = FastAPI(debug=True)

base_dir = os.path.dirname(__file__)
config_file_path = os.path.join(base_dir, 'config.ini')
logging_config_file_path = os.path.join(base_dir, 'logging.conf')

config = configparser.ConfigParser()
config.read(config_file_path)

username = config.get('SETTINGS', 'username')
password_hash = config.get('SETTINGS', 'password_hash')
log_level = config.get('SETTINGS', 'log_level')
log_path = config.get('SETTINGS', 'log_path')

fileConfig('server/src/http_server/logging.conf', defaults={'log_path': log_path})
logger = logging.getLogger('app')


security = HTTPBasic()


def get_settings():
    return config['SETTINGS']


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    except HTTPException as exc:
        logger.exception("HTTPException: %s", exc)
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


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != username or credentials.password != password_hash:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/students/", response_model=str)
async def create_student(
        student: schemas.StudentCreate,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(authenticate)):
    try:
        if crud.create_student(db, student):
            logger.info("Student created successfully: %s", student.name)
            return "Student created successfully"
    except Exception as e:
        logger.exception("Error in create_student endpoint: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/students/{student_id}/photo", response_model=str)
async def upload_photo(
        student_id: int,
        photo: UploadFile = File(...),
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(authenticate)):
    try:
        if crud.upload_photo(db, student_id, photo.file.read()):
            logger.info("Photo uploaded successfully for student ID: %d", student_id)
            return "Photo uploaded successfully"
    except Exception as e:
        logger.exception("Error in upload_photo endpoint: %s", e)
        raise HTTPException(status_code=404, detail="Student not found")


@app.get("/students/", response_model=list[schemas.Student])
async def read_students(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(authenticate)):
    try:
        students = crud.get_students(db, skip=skip, limit=limit)
        for student in students:
            student.photo = base64.b64encode(student.photo).decode("utf-8")
        logger.info("Students retrieved successfully: count=%d", len(students))
        return students
    except Exception as e:
        logger.exception("Error in read_students endpoint: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/students/{student_id}", response_model=schemas.Student)
async def read_student(
        student_id: int,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(authenticate)):
    try:
        db_student = crud.get_student(db, student_id)
        if db_student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        db_student.photo = base64.b64encode(db_student.photo).decode("utf-8")
        logger.info("Student retrieved successfully: %s", db_student.name)
        return db_student
    except Exception as e:
        logger.exception("Error in read_student endpoint: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/students/{student_id}", response_model=str)
async def delete_student(
        student_id: int,
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(authenticate)):
    try:
        if crud.delete_student(db, student_id):
            logger.info("Student deleted successfully: ID=%d", student_id)
            return "Deleted successfully"
    except Exception as e:
        logger.exception("Error in delete_student endpoint: %s", e)
        raise HTTPException(status_code=404, detail="Student not found")
