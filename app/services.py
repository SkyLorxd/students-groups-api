import random
from sqlalchemy import select, insert, delete, update

from app.database import (
    students_table,
    groups_table,
    fetch_one,
    fetch_all,
    execute,
)


def generate_8_digit_id(exists_fn) -> int:
    while True:
        candidate = random.randint(10000000, 99999999)
        if not exists_fn(candidate):
            return candidate


def student_exists(student_id: int) -> bool:
    row = fetch_one(select(students_table.c.id).where(students_table.c.id == student_id).limit(1))
    return row is not None


def group_exists(group_id: int) -> bool:
    row = fetch_one(select(groups_table.c.id).where(groups_table.c.id == group_id).limit(1))
    return row is not None


def generate_student_id() -> int:
    return generate_8_digit_id(student_exists)


def generate_group_id() -> int:
    return generate_8_digit_id(group_exists)


def create_student(student_name: str) -> dict:
    student_id = generate_student_id()
    execute(
        insert(students_table).values(
            id=student_id,
            students_name=student_name,
            group_id=None,
        )
    )
    return {"id": student_id, "name": student_name, "group_id": None}


def get_student(student_id: int) -> dict | None:
    row = fetch_one(
        select(students_table.c.id, students_table.c.students_name, students_table.c.group_id)
        .where(students_table.c.id == student_id)
    )
    if not row:
        return None
    return {"id": int(row[0]), "name": row[1], "group_id": (int(row[2]) if row[2] is not None else None)}


def list_students() -> list[dict]:
    rows = fetch_all(select(students_table.c.id, students_table.c.students_name, students_table.c.group_id).order_by(students_table.c.id))
    result = []
    for r in rows:
        result.append({"id": int(r[0]), "name": r[1], "group_id": (int(r[2]) if r[2] is not None else None)})
    return result


def delete_student(student_id: int) -> bool:
    rc = execute(delete(students_table).where(students_table.c.id == student_id))
    return rc > 0


def create_group(group_number: str) -> dict:
    group_id = generate_group_id()
    execute(insert(groups_table).values(id=group_id, group_number=group_number))
    return {"id": group_id, "group_number": group_number}


def get_group(group_id: int) -> dict | None:
    row = fetch_one(select(groups_table.c.id, groups_table.c.group_number).where(groups_table.c.id == group_id))
    if not row:
        return None
    return {"id": int(row[0]), "group_number": row[1]}


def list_groups() -> list[dict]:
    rows = fetch_all(select(groups_table.c.id, groups_table.c.group_number).order_by(groups_table.c.id))
    return [{"id": int(r[0]), "group_number": r[1]} for r in rows]


def delete_group(group_id: int) -> bool:
    rc = execute(delete(groups_table).where(groups_table.c.id == group_id))
    return rc > 0


def add_student_to_group(student_id: int, group_id: int) -> bool:
    if not student_exists(student_id) or not group_exists(group_id):
        return False
    rc = execute(update(students_table).where(students_table.c.id == student_id).values(group_id=group_id))
    return rc > 0


def remove_student_from_group(student_id: int, group_id: int) -> bool:
    row = fetch_one(select(students_table.c.group_id).where(students_table.c.id == student_id))
    if not row:
        return False
    current_gid = row[0]
    if current_gid is None or int(current_gid) != int(group_id):
        return False
    rc = execute(update(students_table).where(students_table.c.id == student_id).values(group_id=None))
    return rc > 0


def get_students_in_group(group_id: int) -> list[dict] | None:
    if not group_exists(group_id):
        return None
    rows = fetch_all(
        select(students_table.c.id, students_table.c.students_name, students_table.c.group_id)
        .where(students_table.c.group_id == group_id)
        .order_by(students_table.c.id)
    )
    return [{"id": int(r[0]), "name": r[1], "group_id": int(r[2])} for r in rows]


def transfer_student(student_id: int, from_group_id: int, to_group_id: int) -> bool:
    if not student_exists(student_id):
        return False
    if not group_exists(from_group_id) or not group_exists(to_group_id):
        return False

    row = fetch_one(select(students_table.c.group_id).where(students_table.c.id == student_id))
    if not row:
        return False

    current_gid = row[0]
    if current_gid is None or int(current_gid) != int(from_group_id):
        return False

    rc = execute(update(students_table).where(students_table.c.id == student_id).values(group_id=to_group_id))
    return rc > 0
