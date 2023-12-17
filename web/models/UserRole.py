from ..database import db


class UserRole:
    def __init__(self, id=None, user_id=None, role_name=None):
        self.id = id
        self.user_id = user_id
        self.role_name = role_name

    @classmethod
    def find_by_role_name(cls, role_name):
        sql = "SELECT * FROM user_role WHERE role_name = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (role_name,))
        rows = cur.fetchall()
        return [cls(**row) for row in rows]

    @classmethod
    def insert_user_role(cls, user_id, role_name):
        sql = "INSERT INTO user_role (user_id, role_name) VALUES (%s, %s)"
        params = [user_id, role_name]

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.lastrowid


    @classmethod
    def update_user_role(cls, id, user_id, role_name):
        sql = "UPDATE user_role SET user_id = %s, role_name = %s WHERE id = %s"
        params = [user_id, role_name, id]

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

    @classmethod
    def delete_user_role(cls, id):
        sql = "DELETE FROM user_role WHERE id = %s"
        cur = db.new_cursor()
        cur.execute(sql, (id,))
        db.connection.commit()


    @classmethod
    def check_user_role(cls, user_id, role_name):
        sql = """
            SELECT ur.* FROM user_role ur
            JOIN role r ON ur.role_name = r.name
            WHERE ur.user_id = %s AND r.name = %s
        """
        params = [user_id, role_name]

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        row = cur.fetchone()

        return row is not None
        
    @classmethod
    def check_user_role_by_email(cls, email, role_name):
        sql = """
            SELECT ur.* FROM user_role ur
            JOIN role r ON ur.role_name = r.name
            JOIN user u ON ur.user_id = u.id
            WHERE u.email = %s AND r.name = %s
        """
        params = [email, role_name]

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        row = cur.fetchone()

        return row is not None

    @classmethod
    def check_user_role_by_username(cls, username, role_name):
        sql = """
            SELECT ur.* FROM user_role ur
            JOIN role r ON ur.role_name = r.name
            JOIN user u ON ur.user_id = u.id
            WHERE u.username = %s AND r.name = %s
        """
        params = [username, role_name]

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        row = cur.fetchone()

        return row is not None
