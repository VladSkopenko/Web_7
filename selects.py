from sqlalchemy import func, desc
from models import Teacher, Subject, Student, Rating, Group

from connect_db import session


def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    return session.query(Student.id, Student.name, func.avg(Rating.grade).label("average_grade")) \
        .join(Rating, Student.id == Rating.student_id) \
        .group_by(Student.id, Student.name) \
        .order_by(func.avg(Rating.grade).desc()) \
        .limit(5).all()


def select_2(discipline_id):
    # Знайти студента із найвищим середнім балом з певного предмета.
    return session.query(Student.id, Student.name, Subject.name, func.avg(Rating.grade).label("average_grade")) \
        .join(Rating, Student.id == Rating.student_id) \
        .join(Subject, Rating.subject_id == Subject.id) \
        .filter(Subject.id == discipline_id) \
        .group_by(Student.id, Student.name, Subject.name) \
        .order_by(func.avg(Rating.grade).desc()) \
        .limit(1).all()


def select_3(sub_id):
    # Знайти середній бал у групах з певного предмета.
    return session.query(Group.name, Subject.name, func.avg(Rating.grade).label("average_grade")) \
        .join(Student, Group.id == Student.group_id) \
        .join(Rating, Student.id == Rating.student_id) \
        .join(Subject, Rating.subject_id == Subject.id) \
        .filter(Subject.id == sub_id) \
        .group_by(Group.name, Subject.name).all()

def select_4():
    pass


def select_5():
    pass


def select_6():
    pass


def select_7():
    pass


def select_8():
    pass


def select_9():
    pass


def select_10():
    pass


def select_11():
    pass


def select_12():
    pass

for name in select_1():
    print(name)
print(select_2(3))
print(select_3(1))