from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

app = FastAPI()

# Define the database URL, change it according to your database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic models for requests and responses
class StudentCreate(BaseModel):
    date_of_birth: str
    place_of_birth: str
    year_of_enrollment: int


class Student(BaseModel):
    id: int
    date_of_birth: str
    place_of_birth: str
    year_of_enrollment: int

    class Config:
        orm_mode = True


# SQLAlchemy models
class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    date_of_birth = Column(Date, index=True)
    place_of_birth = Column(String, index=True)
    year_of_enrollment = Column(Integer, index=True)


Base.metadata.create_all(bind=engine)


@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = StudentModel(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    for var, value in vars(student).items():
        setattr(db_student, var, value) if value else None
    db.commit()
    db.refresh(db_student)
    return db_student


@app.delete("/students/{student_id}", response_model=Student)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return db_student
