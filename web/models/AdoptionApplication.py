import datetime

from ..database import \
    db  # Make sure to import your database module or connection here


class AdoptionApplication:
    def __init__(self, id=None, user_id=None, animal_id=None, application_date=None,
                 status='Pending', reason_to_adopt=None, is_active=None, admin_notes=None):
        self.id = id
        self.user_id = user_id
        self.animal_id = animal_id
        self.application_date = application_date or datetime.datetime.now()
        self.status = status
        self.reason_to_adopt = reason_to_adopt
        self.is_active = is_active
        self.admin_notes = admin_notes

    @classmethod
    def find_by_id(cls, application_id):
        sql = "SELECT * FROM adoption_application WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (application_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)

    @classmethod
    def insert(cls, application):
        sql = """
            INSERT INTO adoption_application 
            (user_id, animal_id, application_date, status, reason_to_adopt, admin_notes) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur = db.new_cursor()
        cur.execute(sql, (
            application.user_id,
            application.animal_id,
            application.application_date,
            application.status,
            application.reason_to_adopt,
            application.admin_notes
        ))
        db.connection.commit()

    @classmethod
    def set_all_under_review(cls, animal_id):
        sql = """
            UPDATE adoption_application
            SET status = 'Under Review'
            WHERE animal_id = %s
        """
        cur = db.new_cursor()
        cur.execute(sql, (animal_id,))
        db.connection.commit()

    @classmethod
    def set_under_review(cls, animal_id, user_id):
        sql = """
            UPDATE adoption_application
            SET status = 'Under Review'
            WHERE animal_id = %s AND user_id = %s
        """
        cur = db.new_cursor()
        cur.execute(sql, (animal_id, user_id))
        db.connection.commit()

    @classmethod
    def set_approved_and_reject_others(cls, animal_id, user_id):
        sql_reject_others = """
            UPDATE adoption_application
            SET status = 'Rejected'
            WHERE animal_id = %s AND user_id != %s
        """
        cur_reject_others = db.new_cursor()
        cur_reject_others.execute(sql_reject_others, (animal_id, user_id))

        # Approve the specified application
        sql_approve = """
            UPDATE adoption_application
            SET status = 'Approved'
            WHERE animal_id = %s AND user_id = %s
        """
        cur_approve = db.new_cursor()
        cur_approve.execute(sql_approve, (animal_id, user_id))

        db.connection.commit()

    @classmethod
    def set_rejected(cls, animal_id, user_id):
        sql = """
            UPDATE adoption_application
            SET status = 'Rejected'
            WHERE animal_id = %s AND user_id = %s
        """
        cur = db.new_cursor()
        cur.execute(sql, (animal_id, user_id))
        db.connection.commit()

    @classmethod
    def set_turnovered(cls, animal_id, user_id):
        sql = """
            UPDATE adoption_application
            SET status = 'Turnovered'
            WHERE animal_id = %s AND user_id = %s
        """
        cur = db.new_cursor()
        cur.execute(sql, (animal_id, user_id))
        animal_sql = """
            UPDATE animal
            SET is_adopted = 1,
                for_adoption = 0,
                in_shelter = 0
            WHERE id = %s
        """
        cur.execute(animal_sql, (animal_id,))
        db.connection.commit()

    @staticmethod
    def get_user_applications(user_id):
        sql = """
                SELECT * 
                FROM adoption_application 
                LEFT JOIN animal ON adoption_application.animal_id = animal.id
                WHERE adoption_application.user_id = %s
            """        
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        rows = cur.fetchall()
        return rows

    @staticmethod
    def get_animals_applications():
        sql = """
                SELECT 
                    animal.*, 
                    COUNT(adoption_application.user_id) AS user_count
                FROM animal 
                LEFT JOIN adoption_application ON adoption_application.animal_id = animal.id
                WHERE animal.is_adopted = 0 and animal.for_adoption = 1
                GROUP BY animal.id
            """   
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    @staticmethod
    def get_animal_applications(animal_id):
        sql = """
                SELECT *
                FROM adoption_application 
                LEFT JOIN user ON adoption_application.user_id = user.id
                WHERE adoption_application.animal_id = %s
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (animal_id,))
        rows = cur.fetchall()
        return rows

    @staticmethod
    def get_applications():
        sql = "SELECT * FROM adoption_application"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
        return [AdoptionApplication(**row) for row in rows]
    
    @classmethod
    def find_by_user_animal(cls, user_id, animal_id):
        sql = "SELECT * FROM adoption_application WHERE user_id = %s AND animal_id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id, animal_id))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)
