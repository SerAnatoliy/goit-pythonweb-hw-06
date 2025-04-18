from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=False)
    group: Mapped["Group"] = relationship(back_populates='students')
    grades: Mapped[list["Grade"]] = relationship(back_populates="student")

class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    students: Mapped[list["Student"]] = relationship(back_populates="group")

class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    subjects: Mapped[list["Subject"]] = relationship(back_populates="teacher")

class Subject(Base):
    __tablename__ = 'subjects'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'), nullable=False)
    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")
    grades: Mapped[list["Grade"]] = relationship(back_populates="subject")

class Grade(Base):
    __tablename__ = 'grades'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'), nullable=False)
    grade: Mapped[float] = mapped_column(nullable=False)
    date_received: Mapped[date] = mapped_column(nullable=False)
    student: Mapped["Student"] = relationship(back_populates="grades")
    subject: Mapped["Subject"] = relationship(back_populates="grades")