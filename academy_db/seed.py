from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from academy_db.models import Base, Student, Group, Teacher, Subject, Grade
from academy_db.database_config import url_to_db
import random
from datetime import datetime, timedelta

# Створення двигуна та сесії
engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()

faker = Faker()

def seed_database():
    # Create groups
    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)
    session.commit()

    # Create teachers
    teachers = [Teacher(name=faker.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()

    # Create subjects
    subjects = [Subject(name=faker.word(), teacher=random.choice(teachers)) for _ in range(8)]
    session.add_all(subjects)
    session.commit()

    # Create students
    students = [Student(name=faker.name(), group=random.choice(groups)) for _ in range(50)]
    session.add_all(students)
    session.commit()

    # Create grades
    for student in students:
        for subject in subjects:
            for _ in range(20):
                grade = Grade(
                    student=student,
                    subject=subject,
                    grade=random.uniform(60, 100),
                    date_received=datetime.now() - timedelta(days=random.randint(1, 100))
                )
                session.add(grade)
    session.commit()

if __name__ == "__main__":
    seed_database()