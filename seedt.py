from connect_db import session
from models import Teacher, Subject, Student, Rating, Group
import faker
from sqlalchemy import select
from datetime import date, datetime, timedelta
from random import randint, choice

fake = faker.Faker('uk_UA')
group_name = ["Група_1", "Група_2", "Група_3"]
subjects_name = ["Математика", "Программирование", "Финансы", "Банковское дело", "Страхование"]

def seed_teacher():
    for _ in range(3):
        teacher = Teacher(name=fake.name())
        session.add(teacher)
    session.commit()

def seed_group():
    for name in group_name:
        group = Group(name=name)
        session.add(group)
    session.commit()

def seed_subject():
    teacher_idi = session.scalars(select(Teacher.id)).all()
    for name in subjects_name:
        subject = Subject(name=name, teacher_id=choice(teacher_idi))
        session.add(subject)
    session.commit()


def seed_student():
    group_numbers = session.scalars(select(Group.id)).all()
    for _ in range(35):
        student = Student(name=fake.name(), group_id=choice(group_numbers))
        session.add(student)
    session.commit()

def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result

def seed_rating():
    start_date = datetime.strptime("2023-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2024-02-14", "%Y-%m-%d")
    d_range = date_range(start=start_date, end=end_date)
    discipline_id_select = session.scalars(select(Subject.id)).all()
    student_id_select = session.scalars(select(Student.id)).all()

    for d in d_range:
        random_id_discipline = choice(discipline_id_select)
        random_ids_student = [choice(student_id_select) for _ in range(5)]
        for student_id in random_ids_student:
            grade = Rating(
                grade=randint(1, 100),
                date_of=d,
                student_id=student_id,
                subject_id=random_id_discipline,
            )
            session.add(grade)
    session.commit()
def main():
    seed_teacher()
    seed_group()
    seed_subject()
    seed_student()
    seed_rating()

if __name__ == "__main__":
    main()


