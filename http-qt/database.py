from sqlalchemy import create_engine, Column, Integer, String, Date, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345678@localhost/http-qt"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_of_birth = Column(Date)
    photo = Column(LargeBinary)
    grade = Column(Integer)
    student_group = Column(String)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
