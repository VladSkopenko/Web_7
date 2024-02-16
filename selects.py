from sqlalchemy import func, select, and_
from models import Teacher, Subject, Student, Rating, Group
from krasota import vizualization
from connect_db import session
import  logging


logging.basicConfig(level=logging.DEBUG)

@vizualization
def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    return session.query(Student.id, Student.name, func.avg(Rating.grade).label("average_grade")) \
        .join(Rating, Student.id == Rating.student_id) \
        .group_by(Student.id, Student.name) \
        .order_by(func.avg(Rating.grade).desc()) \
        .limit(5).all()

@vizualization
def select_2(discipline_id):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    return session.query(Student.id, Student.name, Subject.name, func.avg(Rating.grade).label("average_grade")) \
        .join(Rating, Student.id == Rating.student_id) \
        .join(Subject, Rating.subject_id == Subject.id) \
        .filter(Subject.id == discipline_id) \
        .group_by(Student.id, Student.name, Subject.name) \
        .order_by(func.avg(Rating.grade).desc()) \
        .limit(1).all()

@vizualization
def select_3(sub_id):
    """Знайти середній бал у групах з певного предмета."""
    return session.query(Group.name, Subject.name, func.avg(Rating.grade).label("average_grade")) \
        .join(Student, Group.id == Student.group_id) \
        .join(Rating, Student.id == Rating.student_id) \
        .join(Subject, Rating.subject_id == Subject.id) \
        .filter(Subject.id == sub_id) \
        .group_by(Group.name, Subject.name).all()
@vizualization
def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)"""
    return session.query(func.avg(Rating.grade).label("average_grade")).scalar()

@vizualization
def select_5(t_id):
    """ Знайти які курси читає певний викладач."""
    return session.query(Teacher.name, Subject.name) \
        .select_from(Subject).join(Teacher).filter(Teacher.id == t_id) \
        .group_by(Subject.name, Teacher.name).all()


@vizualization
def select_6(g_id):
    """Знайти список студентів у певній групі."""
    return session.query(Group.name, Student.name) \
        .select_from(Student).join(Group).filter(Student.group_id == g_id) \
        .group_by(Student.name,Group.name).all()

@vizualization
def select_7(id_subj, id_grou):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    return session.query(Student.name, Rating.grade, Subject.name) \
        .join(Group, Student.group_id == Group.id) \
        .join(Rating, Student.id == Rating.student_id) \
        .join(Subject, Rating.subject_id == Subject.id) \
        .filter(Group.id == id_grou, Subject.id == id_subj) \
        .all()

@vizualization
def select_8(t_id):
    """ Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    return session.query(Subject.name, Teacher.name, func.avg(Rating.grade)) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .join(Rating, Subject.id == Rating.subject_id) \
        .filter(Teacher.id == t_id) \
        .group_by(Subject.name, Teacher.name) \
        .all()
@vizualization
def select_9(stud_id):
    """Знайти список курсів, які відвідує певний студент."""
    return session.query(Student.name, Subject.name, Rating.grade) \
        .join(Rating, Student.id == Rating.student_id) \
        .join(Subject, Rating.subject_id == Subject.id) \
        .filter(Student.id == stud_id) \
        .all()

@vizualization
def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач."""
    return session.query(Subject.name, Student.name, Teacher.name) \
        .join(Rating, Subject.id == Rating.subject_id) \
        .join(Student, Rating.student_id == Student.id) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Student.id == student_id, Teacher.id == teacher_id) \
        .distinct() \
        .all()

@vizualization
def select_11(t_id, s_id):
    """ Середній бал, який певний викладач ставить певному студентові."""
    return session.query(Subject.name, Student.name, Teacher.name, func.avg(Rating.grade).label("average_grade")) \
        .join(Subject, Rating.subject_id == Subject.id) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .join(Student, Rating.student_id == Student.id) \
        .filter(Teacher.id == t_id, Student.id == s_id) \
        .group_by(Subject.name, Student.name, Teacher.name) \
        .all()




@vizualization
def select_12(group_id, discipline_id):
    """Оценки студентов в определенной группе по определенному предмету на последнем занятии."""
    subquery = (select(func.max(Rating.date_of))
                .join(Student).join(Group)
                .filter(and_(Group.id == group_id, Rating.subject_id == discipline_id))
                .scalar_subquery())
    result = (session.query(Group.name, Student.name, Subject.name, Rating.grade, Rating.date_of)
              .select_from(Rating)
              .join(Subject)
              .join(Student)
              .join(Group)
              .filter(and_(Group.id == group_id, Subject.id == discipline_id, Rating.date_of == subquery))
              .order_by(Student.name)
              .all())
    return result

logging.basicConfig(level=logging.DEBUG)
select_1()
select_2(3)
select_3(1)
select_5(1)
select_6(1)
select_7(1, 1)
select_8(1)
select_9(1)

select_10(1,1)
select_11(1,1 )
select_12(1,1)


