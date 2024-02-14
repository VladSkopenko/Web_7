from sqlalchemy import func, desc
from models import Teacher, Subject, Student, Rating, Group

from connect_db import session


def select_1():
    return (session.query(Student.name, func.round(func.avg(Rating.grade), 2).label('avg_grade'))\
            .select_from(Rating).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all())


def select_2(discipline_id):
    return session.query(Student.name, Subject.name, func.round(func.avg(Rating.grade), 2).label("average_grade")) \
        .select_from(Rating).join(Student).join(Subject).filter(Subject.id == discipline_id) \
        .group_by(Student.id, Subject.name).order_by(desc('average_grade')).limit(1).all()


def select_3():
    pass


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
