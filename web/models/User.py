import datetime

from flask_login import UserMixin

from ..database import db


class User(UserMixin):
    def __init__(
            self, 
            email: str = None, 
            google_id: str = None, 
            username: str = None, 
            first_name: str = None, 
            last_name: str = None, 
            gender: str = None,
            password: str = None, 
            photo_url: str | None = None, 
            contact_number: str = None, 
            is_verified: bool = False, 
            unread_notification_count: int = 0,
            roles: [str] = [], 
            id: int | None = None, 
            created_at: datetime.date | None = None):
        self.id = id
        self.email = email
        self.google_id = google_id
        self.username = username
        self.first_name = first_name
        self.gender = gender
        self.last_name = last_name
        self.password = password
        self.is_verified = is_verified
        self.photo_url = photo_url
        self.contact_number = contact_number
        self.unread_notification_count = unread_notification_count
        self.roles = roles
        self.created_at = created_at
    
    @classmethod
    def find_all(cls, page_number: int, page_size: int, filters: dict = None):
        offset = (page_number - 1) * page_size

        where_clauses = []
        filter_params = []

        if filters: 
            for key, value in filters.items():
                if not value:
                    continue

                if key == "query":
                    where_clauses.append("first_name LIKE %s OR last_name LIKE %s OR email LIKE %s OR username LIKE %s")
                    filter_params.extend([f"%{value}%", f"%{value}%", f"%{value}%", f"%{value}%"])
                    continue
    
                where_clauses.append(f"{key} = %s")
                filter_params.append(value)

        where_clauses.append("username != %s")
        filter_params.append("admin")
        
        where_clause = " AND ".join(where_clauses) if where_clauses else ""

        sql = f"""
            SELECT 
                *
            FROM user
            LEFT JOIN 
                user_role ON user.id = user_role.user_id
            """

        if where_clause:
            sql += f" WHERE {where_clause}"
        
        sql += " LIMIT %s OFFSET %s"

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, filter_params + [page_size, offset])
        data = cur.fetchall()

        count_sql = """
            SELECT
                COUNT(*) as total_count
            FROM user
        """

        if where_clause:
            count_sql += f" WHERE {where_clause}"

        cur.execute(count_sql, filter_params)
        total_count = cur.fetchone()['total_count']

        return {
            'data': data,
            'total_count': total_count,
            'offset': offset
        }
        
    
    @classmethod
    def find_by_id(cls, user_id: int):
        sql = "SELECT * FROM user WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)    
    
    @staticmethod
    def find_members():
        sql = """
            SELECT 
                user.id
            FROM user
            LEFT JOIN
                user_role ON user.id = user_role.user_id
            WHERE 
                user_role.role_name = 'Member'
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql)
        members = cur.fetchall()
        return members

    
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
            ) VALUES (%(email)s, %(username)s, %(first_name)s, %(last_name)s, %(password)s, %(photo_url)s, %(contact_number)s)
        """
        params = {
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'password': user.password,
            'photo_url': user.photo_url,
            'contact_number': user.contact_number,
        }            

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.lastrowid
    
    @classmethod
    def update(cls, user):
        sql = """
            UPDATE user
            SET
                email=%(email)s,
                username=%(username)s,
                first_name=%(first_name)s,
                last_name=%(last_name)s,
                photo_url=%(photo_url)s,
                contact_number=%(contact_number)s
            WHERE id=%(id)s
        """

        params = {
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'photo_url': user.photo_url,
            'contact_number': user.contact_number,
            'id': user.id
        }

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.rowcount

    @classmethod
    def delete(cls, id):
        sql =  """
            DELETE FROM user
            WHERE id = %(id)s
        """
        cur = db.new_cursor()
        cur.execute(sql, {'id': id})
        db.connection.commit()

    
    @classmethod
    def update_email(cls, email, user_id):
        sql = """
            UPDATE user
            SET email = %(email)s
            WHERE id = %(user_id)s
        """

        params = {
            'email': email, 
            'user_id': user_id
        }

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        db.connection.commit()


    @staticmethod
    def set_is_verified(user_id):
        sql = """
            UPDATE user
            SET is_verified = 1
            WHERE id = %(user_id)s
        """

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, {'user_id': user_id})
        db.connection.commit()

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


    