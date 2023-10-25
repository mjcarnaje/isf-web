import datetime
from flask_login import UserMixin
from ..database import db

class Admin(UserMixin):
    def __init__(self, email: str = None, username: str = None, password: str = None, id: int | None = None, created_at: datetime.datetime | None = None):
        self.id = id
        self.email = email
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    @staticmethod
    def insert_ignore(email: str, username: str, password: str):
        sql = "INSERT IGNORE INTO admin (email, username, password) VALUES (%s, %s, %s)"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (email, username, password))
        db.connection.commit()
        return cur.lastrowid

    @staticmethod
    def find_by_id(user_id: int):
        sql = "SELECT * FROM admin WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        return row
    
    @classmethod
    def find_by_username(cls, username: str):
        sql = "SELECT * FROM admin WHERE username = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (username,))
        admin = cur.fetchone()
        if not admin: 
            return None
        return cls(**admin)

    