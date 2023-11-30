from pydantic import BaseModel
from datetime import date


class Student(BaseModel):
    id: int
    city: str
    name: str
    birthdate: date
    year_of_enrollment: date


class Faculty(BaseModel):

    id: int
    name: str
    decan: str
    count: int


class Education(BaseModel):

    id: int
    student_id: int
    faculty_id: int
    group: int
    year: int
    sum: int
    speciality: str


class Config:
    orm_mode = True
