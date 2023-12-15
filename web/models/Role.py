import datetime

from flask_login import UserMixin

from ..database import db


class Role(UserMixin):
    def __init__(self, name: str = None, id: str | None  = None):
        self.id = id
        self.name = name

    @classmethod
    def find_by_id(cls, role_name: int):
        sql = "SELECT * FROM role WHERE id  = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (role_name,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)

    @classmethod
    def find_all(cls):
        sql = "SELECT * FROM role"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
        return [cls(**row) for row in rows]

    @classmethod
    def insert_role(cls, role_name: str):
        sql = "INSERT INTO role (name) VALUES (%s)"
        params = [role_name]

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.lastrowid

    @classmethod
    def update_role(cls, role_name: int, new_name: str):
        sql = "UPDATE role SET name = %s WHERE id = %s"
        params = [new_name, role_name]

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

    @classmethod
    def delete_role(cls, role_name: int):
        sql = "DELETE FROM role WHERE id = %s"
        cur = db.new_cursor()
        cur.execute(sql, (role_name,))
        db.connection.commit()

    @staticmethod
    def check_if_role_exists(name: str, id: int = None):
        sql = "SELECT * FROM role WHERE name=%s"
        params = [name]
        if id:
            sql += " AND id != %s"
            params.append(id)
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        exists = cur.fetchone() is not None
        return exists
