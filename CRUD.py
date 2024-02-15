from datetime import datetime, timedelta
import logging

from sqlalchemy.exc import SQLAlchemyError

import argparse
import random

from models import Teacher, Student, Group, Subject, Rating
from connect_db import session

logging.basicConfig(level=logging.INFO)


def random_date(start_date, end_date, result=None) -> datetime:
    """
    Функція приймає дату початку та кінець періоду, та випадково повертає робочий день (з понеділка по п'ятницю)
    у форматі дати.
    """
    start_datetime = datetime.strptime(start_date, "%Y.%m.%d")
    end_datetime = datetime.strptime(end_date, "%Y.%m.%d")
    delta_days = (end_datetime - start_datetime).days
    random_days = random.randint(0, delta_days)
    fix_days = random.randint(1, 4)
    random_date_var = start_datetime + timedelta(days=random_days)
    if random_date_var.isoweekday() < 6:
        result = random_date_var
    else:
        result = random_date_var + timedelta(days=fix_days)
    return result.strftime("%Y.%m.%d")


def create_record(model, name, model_name=None):
    """
    Функція приймає два аргументи - 'model', та 'name'(дані) шукає у пакеті моделей відповідну модель запису у SQL BD,
    та створює новий запис у БД відповідно до умов моделі.
    """
    if model == "Rating":
        student_ids = session.query(Student.id).all()
        subject_ids = session.query(Subject.id).all()
        model_name = eval(model)(
            grade=name,
            student_id=random.choice(student_ids)[0],
            subject_id=random.choice(subject_ids)[0],
            date_of=random_date("2023-09-01", "2024-02-14"),
        )

    elif model == "Teacher":
        model_name = eval(model)(name=name)
    elif model == "Student":
        group_ids = session.query(Group.id).all()
        model_name = eval(model)(name=name, group_id=random.choice(group_ids)[0])
    elif model == "Group":
        model_name = eval(model)(name=name)
    elif model == "Subject":
        teacher_ids = session.query(Teacher.id).all()
        model_name = eval(model)(name=name, teacher_id=random.choice(teacher_ids)[0])
    try:
        session.add(model_name)
    except SQLAlchemyError as e:
        print(f"Ooops: ", e)
        session.rollback()
    finally:
        session.commit()
        logging.info(
            f'New {model}: "{name}" successfully added to table {model.lower()}s'
        )


def list_records(model):
    """
    Функція приймає агрумент 'model' та повертає список усіх наявних даних з відповідної таблиці
    """
    result = session.query(eval(model)).all()
    if model == "Rating":
        for r in result:
            print(f"ID: {r.id} | Grade: {r.grade} | Grade date: {r.date_of}")
    elif model in ["Student", "Teacher"]:
        for r in result:
            print(f"ID: {r.id} | {model} name: {r.name}")
    else:
        for r in result:
            print(f"ID: {r.id} | {model} name: {r.name}")


def update_record(model, ids, name):
    """
    Функція приймає агрументи: 'model',  'ids' (ключ), 'name'(дані) та на основі отриманих даних вносить зміну до
    відповідного запису за отриманим ключем в базі даних
    """
    model_class = eval(model)
    model_update = session.get(model_class, ids)
    if model_update:

        if model in ["Student", "Teacher"]:
            model_update.name = name
        elif model == "Rating":
            model_update.grade = name
        else:
            model_update.name = name
        try:
            session.add(model_update)
            logging.info(
                f"Table: {model.lower()}s with ID: {ids} was successfully updated with new data: {name}"
            )
        except SQLAlchemyError as e:
            print("Ooops...", e)
            session.rollback()
        finally:
            session.commit()


def remove_record(model, ids):
    """
    Функція приймає два аргументи: 'model' та 'ids'(ключ), знаходить відповідний до ключу запис у відповідній таблиці
    в базі даних та видаляє його.
    """
    model_remove = session.get(eval(model), ids)
    try:
        session.delete(model_remove)
    except SQLAlchemyError as e:
        print(f"Ooops: ", e)
        session.rollback()
    finally:
        session.commit()
        logging.info(
            f"Entry with ID: {ids} was successfully deleted from table: {model}s"
        )


def main():
    parser = argparse.ArgumentParser(
        description="CLI програма для CRUD операцій із базою даних"
    )
    parser.add_argument(
        "-a",
        "--action",
        choices=["create", "list", "update", "remove"],
        help="Дія для виконання: create, list, update, remove",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=["Teacher", "Group", "Rating", "Student", "Subject"],
        help="Модель, над якою виконується операція",
        required=True,
    )
    parser.add_argument(
        "-id",
        "--record_id",
        type=int,
        help="Ключ запису для оновлення або видалення в БД",
    )
    parser.add_argument(
        "-n", "--name", help="Значення для створення імені, оцінки або оновлення запису"
    )

    args = parser.parse_args()

    if args.action == "create":
        if args.name:
            create_record(args.model, name=args.name)
        else:
            print("Параметр '--name' є обов'язковим для дії 'create'")
    elif args.action == "list":
        list_records(args.model)
    elif args.action == "update":
        if args.record_id and args.name:
            update_record(args.model, ids=args.record_id, name=args.name)
        else:
            print("Параметри '--id' та '--name' є обов'язковими для дії 'update'")
    elif args.action == "remove":
        if args.record_id:
            remove_record(args.model, args.record_id)
        else:
            print("Параметр '--id' є обов'язковим для дії 'remove'")


if __name__ == "__main__":
    main()