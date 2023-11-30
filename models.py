from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey

Base = declarative_base()


class Student(Base):
    __tablename__ = "Student"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    name = Column(String)
    birthdate = Column(Date)
    year_of_enrollment = Column(Integer)


class Faculty(Base):
    __tablename__ = "Faculty"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    decan = Column(String)
    count = Column(Integer)


class Education(Base):
    __tablename__ = "Education"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("Student.id"), primary_key=True, nullable=False)
    faculty_id = Column(Integer, ForeignKey("Faculty.id"), primary_key=True, nullable=False)
    group = Column(Integer)
    year = Column(Integer)
    sum = Column(Integer)
    speciality = Column(String)