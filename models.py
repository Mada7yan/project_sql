from sqlalchemy import Column, ForeignKey, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    date_of_birth = Column(Date)
    place_of_birth = Column(String)
    year_of_enrollment = Column(Integer)
    # Relationships
    education_details = relationship("Education", back_populates="student")


class Education(Base):
    __tablename__ = 'education'
    id = Column(Integer, primary_key=True)
    specialty = Column(String)
    group = Column(String)
    year = Column(Integer)
    degree_sum = Column(Integer)  # Assuming this is an integer field
    student_id = Column(Integer, ForeignKey('students.id'))
    faculty_id = Column(Integer, ForeignKey('faculties.id'))
    # Relationships
    student = relationship("Student", back_populates="education_details")
    faculty = relationship("Faculty", back_populates="education_details")


class Faculty(Base):
    __tablename__ = 'faculties'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dean = Column(String)
    number_of_places = Column(Integer)
    education_details = relationship("Education", back_populates="faculty")


engine = create_engine('sqlite:///project.db')
Base.metadata.create_all(engine)
