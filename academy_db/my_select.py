from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, desc
from academy_db.models import Student, Group, Teacher, Subject, Grade
from academy_db.database_config import url_to_db
from tabulate import tabulate  # Для зручного форматування результатів
from colorama import Fore, Style, init

init(autoreset=True)  # Ініціалізація colorama для автоматичного скидання кольорів

# Налаштування сесії
engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()

def round_result(value, decimals=2):
    """Округлення значення до вказаної кількості десяткових знаків."""
    if isinstance(value, float):
        return round(value, decimals)
    if isinstance(value, list):
        return [(item[0], round(item[1], decimals)) if len(item) > 1 else item for item in value]
    return value

# Функції запитів
def select_1(session):
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return round_result(result) if result else "No data found for top 5 students by average grade"

def select_2(session, subject_name):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .first()
    )
    return {"Student": result[0], "Avg Grade": round_result(result[1])} if result else f"No data found for top student in subject '{subject_name}'"

def select_3(session, subject_name):
    """Знайти середній бал у групах з певного предмета."""
    result = (
        session.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
        .select_from(Group)  # Вказуємо явну стартову таблицю
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.id)
        .all()
    )
    return round_result(result) if result else f"No data found for average grade in groups for subject '{subject_name}'"

def select_4(session):
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    result = session.query(func.avg(Grade.grade).label("avg_grade")).scalar()
    return round_result(result) if result else "No data found for average grade across all records"

def select_5(session, teacher_name):
    """Знайти які курси читає певний викладач."""
    result = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return result if result else f"No courses found for teacher '{teacher_name}'"

def select_6(session, group_name):
    """Знайти список студентів у певній групі."""
    result = (
        session.query(Student.name)
        .join(Group)
        .filter(Group.name == group_name)
        .all()
    )
    return result if result else f"No students found in group '{group_name}'"

def select_7(session, group_name, subject_name):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    result = (
        session.query(Student.name, Grade.grade)
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return round_result(result) if result else f"No grades found for group '{group_name}' in subject '{subject_name}'"

def select_8(session, teacher_name):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    result = (
        session.query(func.avg(Grade.grade).label("avg_grade"))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return round_result(result) if result else f"No data found for average grade assigned by teacher '{teacher_name}'"

def select_9(session, student_name):
    """Знайти список курсів, які відвідує певний студент."""
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .distinct()
        .all()
    )
    return result if result else f"No courses found for student '{student_name}'"

def select_10(session, student_name, teacher_name):
    """Список курсів, які певному студенту читає певний викладач."""
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .distinct()
        .all()
    )
    return result if result else f"No courses found for student '{student_name}' taught by teacher '{teacher_name}'"

# Виконання запитів
def run_queries():
    print(Fore.CYAN + "1. Топ-5 студентів із найвищим середнім балом:")
    result = select_1(session)
    print(tabulate(result, headers=["Student", "Avg Grade"], tablefmt="grid") if isinstance(result, list) else Fore.RED + result)

    print(Fore.CYAN + "\n2. Студент із найвищим середнім балом із предмета (data):")
    result = select_2(session, subject_name="data")
    if isinstance(result, dict):
        print(tabulate([result.values()], headers=result.keys(),
                       tablefmt="grid"))
    else:
        print(Fore.RED + result)

    print(Fore.CYAN + "\n3. Середній бал у групах із предмета (cause):")
    result = select_3(session, subject_name="cause")
    print(tabulate(result, headers=["Group", "Avg Grade"], tablefmt="grid") if isinstance(result, list) else Fore.RED + result)

    print(Fore.CYAN + "\n4. Середній бал на потоці:")
    result = select_4(session)
    print(result if isinstance(result, float) else Fore.RED + result)

    print(Fore.CYAN + "\n5. Курси, які читає викладач (Jason Zavala):")
    result = select_5(session, teacher_name="Jason Zavala")
    print(tabulate(result, headers=["Course"], tablefmt="grid") if isinstance(result, list) else Fore.RED + result)

    print(Fore.CYAN + "\n6. Студенти у групі (Group 1):")
    result = select_6(session, group_name="Group 1")
    print(tabulate(result, headers=["Student"], tablefmt="grid") if isinstance(result, list) else Fore.RED + result)

    print(Fore.CYAN + "\n7. Оцінки студентів у групі (Group 1) з предмета (Math):")
    result = select_7(session, group_name="Group 1", subject_name="Math")
    print(tabulate(result, headers=["Student", "Grade"], tablefmt="grid") if isinstance(result, list) else Fore.RED + result)

    print(Fore.CYAN + "\n8. Середній бал, який ставить викладач (Jennifer Lane):")
    result = select_8(session, teacher_name="Jennifer Lane")
    print(result if isinstance(result, float) else Fore.RED + result)

    print(Fore.CYAN + "\n9. Курси, які відвідує студент (Paul Hill):")
    result = select_9(session, student_name="Paul Hill")
    print(tabulate(result, headers=["Course"], tablefmt="grid") if isinstance(result, list) else Fore.RED + result)

    print(Fore.CYAN + "\n10. Курси, які читає викладач (Jennifer Lane) для студента (Paul Hill):")
    result = select_10(session, student_name="Paul Hill", teacher_name="Jennifer Lane")
    print(tabulate(result, headers=["Course"], tablefmt="grid") if isinstance(result, list) else Fore.RED + result)

if __name__ == "__main__":
    run_queries()