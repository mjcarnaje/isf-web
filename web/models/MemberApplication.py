

from ..database import db


class MemberApplication():
    def __init__(
            self,
            id: int = None,
            user_id: str = None, 
            status: str = None, 
            join_reason: str = None, 
            created_at: str = None, 
            updated_at: str = None,
           ):
        self.id = id
        self.user_id = user_id
        self.status = status
        self.join_reason = join_reason
        self.created_at = created_at
        self.updated_at = updated_at
        
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
                    where_clauses.append("first_name LIKE %s")
                    filter_params.append(f"%{value}%")
                    continue
    
                where_clauses.append(f"{key} = %s")
                filter_params.append(value)
        
        where_clause = " AND ".join(where_clauses) if where_clauses else ""

        sql = """
            SELECT 
                member_application.id as id,
                user_id,
                join_reason,
                photo_url,
                status,
                first_name, last_name
            FROM member_application
            LEFT JOIN 
                user ON user_id = user.id
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
            FROM member_application
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
    def find_by_id(cls, id: int):
        sql = "SELECT * FROM member_application WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)    

    @classmethod
    def find_by_user_id(cls, user_id: int):
        sql = "SELECT * FROM member_application WHERE user_id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)    
    
    @classmethod
    def insert(cls, member_application):
        sql = """
            INSERT INTO member_application (
                user_id, join_reason
            ) VALUES (%(user_id)s, %(join_reason)s)
        """
        params = {
            'user_id': member_application.user_id,
            'join_reason': member_application.join_reason,
        }            

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.lastrowid
    


    
    @classmethod
    def update(cls, member_application):
        sql = """
            UPDATE member_application
            SET join_reason = %(join_reason)s
            WHERE id = %(id)s
        """
        params = {
            'id': member_application.id,
            'join_reason': member_application.join_reason,
        }

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.rowcount
        

    @staticmethod
    def delete(member_application_id):
        sql = "DELETE FROM member_application WHERE id = %s"

        cur = db.new_cursor()
        cur.execute(sql, (member_application_id,))
        db.connection.commit()

        return cur.rowcount
    
    @staticmethod
    def confirm(id):
        print("Confirming..")
        sql = """
            UPDATE member_application
            SET 
                status = 'Confirmed'
            WHERE id = %s
        """
        print("1...")
        cur = db.new_cursor()
        cur.execute(sql, (id,))
        db.connection.commit()
        print("2...")


        return cur.rowcount

    
    @staticmethod
    def reject(id):
        sql = """
            UPDATE member_application
            SET status = 'Rejected'
            WHERE id = %s
        """

        cur = db.new_cursor()
        cur.execute(sql, (id,))
        db.connection.commit()

        return cur.rowcount
