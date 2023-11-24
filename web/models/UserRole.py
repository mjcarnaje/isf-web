from ..database import db


class UserRole:
    def __init__(self, id=None, user_id=None, role_id=None):
        self.id = id
        self.user_id = user_id
        self.role_id = role_id

    @classmethod
    def find_by_user_id(cls, user_id):
        sql = "SELECT * FROM user_role WHERE user_id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        rows = cur.fetchall()
        return [cls(**row) for row in rows]

    @classmethod
    def find_by_role_id(cls, role_id):
        sql = "SELECT * FROM user_role WHERE role_id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (role_id,))
        rows = cur.fetchall()
        return [cls(**row) for row in rows]

    @classmethod
    def insert_user_role(cls, user_id, role_id):
        sql = "INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)"
        params = [user_id, role_id]

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.lastrowid
    
    @classmethod
    def insert_user_role_by_name(cls, user_id, role_name):
        role_sql = "SELECT id FROM role WHERE name = %s"
        role_cur = db.new_cursor()
        role_cur.execute(role_sql, (role_name,))
        role_result = role_cur.fetchone()

        if role_result is None:
            raise ValueError(f"Role with name {role_name} does not exist.")

        role_id = role_result[0]

        sql = "INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)"
        params = [user_id, role_id]

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.lastrowid

    @classmethod
    def update_user_role(cls, id, user_id, role_id):
        sql = "UPDATE user_role SET user_id = %s, role_id = %s WHERE id = %s"
        params = [user_id, role_id, id]

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
            JOIN role r ON ur.role_id = r.id
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
            JOIN role r ON ur.role_id = r.id
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
            JOIN role r ON ur.role_id = r.id
            JOIN user u ON ur.user_id = u.id
            WHERE u.username = %s AND r.name = %s
        """
        params = [username, role_name]

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        row = cur.fetchone()

        return row is not None
