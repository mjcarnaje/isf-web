import datetime

from ..database import db


class Adoption:
    def __init__(self, 
            id=None, 
            user_id=None,
            animal_id=None,
            application_date=None,
            current_status='Pending',
            interview_preference=None,
            interview_preferred_date=None,
            interview_preferred_time=None,
            reason_to_adopt=None,
            is_active=None,
        ):
        self.id = id
        self.user_id = user_id
        self.animal_id = animal_id
        self.application_date = application_date or datetime.datetime.now()
        self.current_status = current_status
        self.interview_preference = interview_preference
        self.interview_preferred_date = interview_preferred_date
        self.interview_preferred_time = interview_preferred_time
        self.reason_to_adopt = reason_to_adopt
        self.is_active = is_active

    @classmethod
    def find_by_id(cls, application_id):
        sql = "SELECT * FROM adoption WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (application_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)

    @classmethod
    def insert(cls, application):
        sql = """
            INSERT INTO adoption 
                (user_id, animal_id, application_date, current_status, interview_preference, interview_preferred_date, interview_preferred_time, reason_to_adopt) 
            VALUES (%(user_id)s, %(animal_id)s, %(application_date)s, %(current_status)s, %(interview_preference)s, %(interview_preferred_date)s, %(interview_preferred_time)s, %(reason_to_adopt)s)
        """
        params = {
            'user_id': application.user_id,
            'animal_id': application.animal_id,
            'application_date': application.application_date,
            'current_status': application.current_status,
            'interview_preference': application.interview_preference, 
            'interview_preferred_date': application.interview_preferred_date,
            'interview_preferred_time': application.interview_preferred_time,
            'reason_to_adopt': application.reason_to_adopt,
        }
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        db.connection.commit()
        return cur.lastrowid

    @classmethod
    def update(cls, application):
        sql = """
            UPDATE adoption 
            SET application_date = %(application_date)s,
                current_status = %(current_status)s,
                interview_preference = %(interview_preference)s,
                interview_preferred_date = %(interview_preferred_date)s,
                interview_preferred_time = %(interview_preferred_time)s,
                reason_to_adopt = %(reason_to_adopt)s
            WHERE user_id = %(user_id)s AND animal_id = %(animal_id)s
        """
        params = {
            'user_id': application.user_id,
            'animal_id': application.animal_id,
            'application_date': application.application_date,
            'current_status': application.current_status,
            'interview_preference': application.interview_preference, 
            'interview_preferred_date': application.interview_preferred_date,
            'interview_preferred_time': application.interview_preferred_time,
            'reason_to_adopt': application.reason_to_adopt,
        }
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        db.connection.commit()


    @classmethod
    def set_all_under_review(cls, animal_id):
        sql = """
            UPDATE adoption
            SET current_status = 'Under Review'
            WHERE animal_id = %s
        """
        cur = db.new_cursor()
        cur.execute(sql, (animal_id,))
        db.connection.commit()

    @classmethod
    def set_under_review(cls, animal_id, user_id, remarks):
        sql = """
            UPDATE adoption
            SET current_status = 'Under Review'
            WHERE animal_id = %(animal_id)s AND user_id = %(user_id)s
        """

        params = {
            'animal_id': animal_id,
            'user_id': user_id
        }

        cur = db.new_cursor()
        id = cur.execute(sql, params)

        sql = """
            INSERT INTO adoption_status_history
                (application_id, previous_status, status, remarks)
            VALUES
                (%(application_id)s, %(previous_status)s, %(status)s, %(remarks)s)
        """

        params = {
            'application_id': id,
            'previous_status': 'Pending',
            'status': 'Under Review', 
            'remarks': remarks
        }

        cur.execute(sql, params)

        db.connection.commit()

    @classmethod
    def set_approved_and_reject_others(cls, animal_id, user_id):
        sql_reject_others = """
            UPDATE adoption
            SET current_status = 'Rejected'
            WHERE animal_id = %s AND user_id != %s
        """
        cur_reject_others = db.new_cursor()
        cur_reject_others.execute(sql_reject_others, (animal_id, user_id))

        # Approve the specified application
        sql_approve = """
            UPDATE adoption
            SET current_status = 'Approved'
            WHERE animal_id = %s AND user_id = %s
        """
        cur_approve = db.new_cursor()
        cur_approve.execute(sql_approve, (animal_id, user_id))

        db.connection.commit()

    @classmethod
    def set_rejected(cls, animal_id, user_id):
        sql = """
            UPDATE adoption
            SET current_status = 'Rejected'
            WHERE animal_id = %s AND user_id = %s
        """
        cur = db.new_cursor()
        cur.execute(sql, (animal_id, user_id))
        db.connection.commit()

    @classmethod
    def set_turnovered(cls, animal_id, user_id):
        sql = """
            UPDATE adoption
            SET current_status = 'Turnovered'
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
                FROM adoption 
                LEFT JOIN animal ON adoption.animal_id = animal.id
                WHERE adoption.user_id = %s
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
                    COUNT(adoption.user_id) AS user_count
                FROM animal 
                LEFT JOIN adoption ON adoption.animal_id = animal.id
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
                FROM adoption 
                LEFT JOIN user ON adoption.user_id = user.id
                WHERE adoption.animal_id = %s
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (animal_id,))
        rows = cur.fetchall()
        return rows

    @staticmethod
    def get_applications():
        sql = "SELECT * FROM adoption"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
        return [Adoption(**row) for row in rows]
    
    @classmethod
    def find_by_user_animal(cls, user_id, animal_id):
        sql = "SELECT * FROM adoption WHERE user_id = %s AND animal_id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id, animal_id))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)
