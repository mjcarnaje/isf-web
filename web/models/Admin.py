from flask_login import UserMixin
from ..database import db

class Admin(UserMixin):
    email: str
    username: str
    password: str
    id: int | None
    
    def __init__(self, email, username, password, id=None):
        self.id = id
        self.email = email
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def insert_ignore(self):
        sql = "INSERT IGNORE INTO admin (email, username, password) VALUES (%s, %s, %s)"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (self.email, self.username, self.password))
        db.connection.commit()
        return True

    @staticmethod
    def find_one(user_id):
        sql = "SELECT * FROM admin WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        db.execute(sql, (user_id,))
        row = cur.fetchone()
        return row
