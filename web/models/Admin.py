import datetime

from flask_login import UserMixin

from ..database import db


class Admin(UserMixin):
    def __init__(self, email: str = None, username: str = None, password: str = None, id: int | None = None, created_at: datetime.datetime | None = None):
        self.id = id
        self.email = email
        self.username = username
        self.password = password

    @staticmethod
    def insert_ignore(email: str, username: str, password: str):
        sql = "INSERT IGNORE INTO admin (email, username, password) VALUES (%s, %s, %s)"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (email, username, password))
        db.connection.commit()
        return cur.lastrowid

    @classmethod
    def find_by_id(cls, user_id: int):
        sql = "SELECT * FROM admin WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)    
    
    @classmethod
    def find_by_username(cls, username: str):
        sql = "SELECT * FROM admin WHERE username = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (username,))
        admin = cur.fetchone()
        if not admin: 
            return None
        return cls(**admin)
    
    @staticmethod
    def check_if_username_exists(username: str, id: int = None):
        sql = "SELECT * FROM admin WHERE username=%s"
        params = [username]
        if id:
            sql += " AND id != %s"
            params.append(id)
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        exists = cur.fetchone() is not None
        return exists


    