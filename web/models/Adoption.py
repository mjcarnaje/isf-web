import datetime

from ..database import db


class Adoption:
    def __init__(self, 
            id=None, 
            user_id=None,
            animal_id=None,
            current_status='Pending',
            interview_preference=None,
            interview_preferred_date=None,
            interview_preferred_time=None,
            reason_to_adopt=None,
            is_active=None,
            zoom_url=None,
            google_meet_url=None,
            phone_number=None,
            created_at=None,
        ):
        self.id = id
        self.user_id = user_id
        self.animal_id = animal_id
        self.current_status = current_status
        self.interview_preference = interview_preference
        self.interview_preferred_date = interview_preferred_date
        self.interview_preferred_time = interview_preferred_time
        self.reason_to_adopt = reason_to_adopt
        self.is_active = is_active
        self.zoom_url = zoom_url
        self.google_meet_url = google_meet_url
        self.phone_number = phone_number
        self.created_at = created_at or datetime.datetime.now()

    @classmethod
    def find_by_id(cls, adoption_id):
        sql = "SELECT * FROM adoption WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (adoption_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)

    @classmethod
    def insert(cls, application):
        sql = """
            INSERT INTO adoption (
                user_id,
                animal_id,
                current_status,
                interview_preference,
                interview_preferred_date,
                interview_preferred_time,
                reason_to_adopt,
                phone_number,
                created_at
            ) 
            VALUES (
                %(user_id)s,
                %(animal_id)s,
                %(current_status)s,
                %(interview_preference)s,
                %(interview_preferred_date)s,
                %(interview_preferred_time)s,
                %(reason_to_adopt)s,
                %(phone_number)s,
                %(created_at)s
            )
        """
        params = {
            'user_id': application.user_id,
            'animal_id': application.animal_id,
            'current_status': application.current_status,
            'interview_preference': application.interview_preference, 
            'interview_preferred_date': application.interview_preferred_date,
            'interview_preferred_time': application.interview_preferred_time,
            'reason_to_adopt': application.reason_to_adopt,
            'phone_number': application.phone_number,
            'created_at': application.created_at
        }
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        db.connection.commit()
        return cur.lastrowid

    @classmethod
    def update(cls, application):
        sql = """
            UPDATE adoption 
            SET 
                current_status = %(current_status)s,
                interview_preference = %(interview_preference)s,
                interview_preferred_date = %(interview_preferred_date)s,
                interview_preferred_time = %(interview_preferred_time)s,
                reason_to_adopt = %(reason_to_adopt)s
                phone_number = %(phone_number)s
                created_at = %(created_at)s,
            WHERE 
                user_id = %(user_id)s AND animal_id = %(animal_id)s
        """
        params = {
            'user_id': application.user_id,
            'animal_id': application.animal_id,
            'current_status': application.current_status,
            'interview_preference': application.interview_preference, 
            'interview_preferred_date': application.interview_preferred_date,
            'interview_preferred_time': application.interview_preferred_time,
            'reason_to_adopt': application.reason_to_adopt,
            'phone_number': application.phone_number,
            'created_at': application.created_at
        }
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        db.connection.commit()

    @staticmethod
    def set_interview(adoption_id, remarks, zoom_url, google_meet_url):
        sql = """
            UPDATE adoption
            SET 
                current_status = 'Interview',
                zoom_url = %(zoom_url)s,
                google_meet_url = %(google_meet_url)s
            WHERE 
                id = %(adoption_id)s
        """

        params = {
            'zoom_url': zoom_url,
            'google_meet_url': google_meet_url,
            'adoption_id': adoption_id
        }

        cur = db.new_cursor()
        cur.execute(sql, params)

        sql = """
            INSERT INTO adoption_status_history (
                adoption_id,
                previous_status,
                status,
                remarks
            )
            VALUES (
                %(adoption_id)s,
                %(previous_status)s,
                %(status)s,
                %(remarks)s
            )
        """

        params = {
            'adoption_id': adoption_id,
            'previous_status': 'Pending',
            'status': 'Interview', 
            'remarks': remarks
        }

        cur.execute(sql, params)

        db.connection.commit()
        
        return cur.lastrowid

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
            SET 
                current_status = 'Approved'
            WHERE 
                animal_id = %s AND user_id = %s
        """
        cur_approve = db.new_cursor()
        cur_approve.execute(sql_approve, (animal_id, user_id))

        db.connection.commit()

    @classmethod
    def set_rejected(cls, animal_id, user_id):
        sql = """
            UPDATE adoption
            SET 
                current_status = 'Rejected'
            WHERE 
                animal_id = %s AND user_id = %s
        """
        cur = db.new_cursor()
        cur.execute(sql, (animal_id, user_id))
        db.connection.commit()

    @classmethod
    def set_turnovered(cls, animal_id, user_id):
        sql = """
            UPDATE adoption
            SET 
                current_status = 'Turnovered'
            WHERE 
                animal_id = %s AND user_id = %s
        """
        cur = db.new_cursor()
        cur.execute(sql, (animal_id, user_id))
        animal_sql = """
            UPDATE animal
            SET 
                is_adopted = 1,
                for_adoption = 0,
                in_shelter = 0
            WHERE 
                id = %s
        """
        cur.execute(animal_sql, (animal_id,))
        db.connection.commit()

    @staticmethod
    def get_user_applications(user_id):
        sql = """
                SELECT 
                    adoption.*,
                    animal.id as animal_id,
                    animal.name as animal_name,
                    animal.photo_url as animal_photo_url,
                    animal.type as animal_type 
                FROM 
                    adoption
                LEFT JOIN 
                    animal ON adoption.animal_id = animal.id
                WHERE 
                    adoption.user_id = %s
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
                LEFT JOIN 
                    adoption ON adoption.animal_id = animal.id
                WHERE 
                    animal.is_adopted = 0 and animal.for_adoption = 1
                GROUP BY 
                    animal.id
            """   
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    @staticmethod
    def get_animal_applications(animal_id):
        sql = """
                SELECT 
                    adoption.*,
                    first_name,
                    last_name,
                    email,
                    contact_number,
                    user.id as user_id
                FROM adoption 
                LEFT JOIN 
                    user ON adoption.user_id = user.id
                WHERE 
                    adoption.animal_id = %s
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
        sql = """SELECT 
                    * 
                FROM adoption 
                WHERE 
                    user_id = %s AND animal_id = %s"""
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id, animal_id))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)
