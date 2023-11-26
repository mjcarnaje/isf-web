import datetime

from flask_login import UserMixin

from ..database import db


class User(UserMixin):
    def __init__(self, email: str = None, google_id: str = None, username: str = None, first_name: str = None, last_name: str = None, password: str = None, photo_url: str | None = None, contact_number: str = None, roles: [str] = [], id: int | None = None, created_at: datetime.date | None = None):
        self.id = id
        self.email = email
        self.google_id = google_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.photo_url = photo_url
        self.contact_number = contact_number
        
    @classmethod
    def find_by_id(cls, user_id: int):
        sql = "SELECT * FROM user WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)    
    
    @classmethod
    def find_by_username(cls, username: str):
        sql = "SELECT * FROM user WHERE username = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (username,))
        user = cur.fetchone()
        if not user: 
            return None
        return cls(**user)
    
    @classmethod
    def insert(cls, user):
        sql = """
            INSERT INTO user (
                email, username, first_name, last_name, password, photo_url, contact_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            user.email,
            user.username,
            user.first_name,
            user.last_name,
            user.password,
            user.photo_url,
            user.contact_number,
        )            

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.lastrowid


    @staticmethod
    def check_if_username_exists(username: str, id: int = None):
        sql = "SELECT * FROM user WHERE username=%s"
        params = [username]
        if id:
            sql += " AND id != %s"
            params.append(id)
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        exists = cur.fetchone() is not None
        return exists

    @staticmethod
    def check_if_email_exists(email: str, id: int = None):
        sql = "SELECT * FROM user WHERE email=%s"
        params = [email]
        if id:
            sql += " AND id != %s"
            params.append(id)
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        exists = cur.fetchone() is not None
        return exists

    @staticmethod
    def check_if_contact_number_exists(contact_number: str, id: int = None):
        sql = "SELECT * FROM user WHERE contact_number=%s"
        params = [contact_number]
        if id:
            sql += " AND id != %s"
            params.append(id)
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        exists = cur.fetchone() is not None
        return exists


    