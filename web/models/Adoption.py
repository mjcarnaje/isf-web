from flask import current_app
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
        current_app.logger.info("Adding adoption..")
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
        current_app.logger.info("Done!")
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
    
    @staticmethod
    def set_rejected(adoption_id, remarks, previous_status):
        sql = """
            UPDATE adoption
            SET 
                current_status = 'Rejected'
            WHERE 
                id = %(adoption_id)s
        """

        params = {
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
            'previous_status': previous_status,
            'status': 'Rejected', 
            'remarks': remarks
        }

        cur.execute(sql, params)
        
        db.connection.commit()

        return cur.lastrowid


    @staticmethod
    def set_approved(adoption_id, remarks, previous_status):
        sql = """
            UPDATE adoption
            SET 
                current_status = 'Approved'
            WHERE 
                id = %(adoption_id)s
        """

        params = {
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
            'previous_status': previous_status,
            'status': 'Approved', 
            'remarks': remarks
        }

        cur.execute(sql, params)
        
        db.connection.commit()

        return cur.lastrowid


    @staticmethod
    def set_turnovered(adoption_id, remarks, previous_status, animal_id):
        sql = """
            UPDATE adoption
            SET 
                current_status = 'Turnovered'
            WHERE 
                id = %(adoption_id)s
        """

        params = {
            'adoption_id': adoption_id
        }
        
        cur = db.new_cursor()
        cur.execute(sql, params)

        sql = """
            UPDATE animal
            SET 
                is_adopted = 1,
                for_adoption = 0,
                in_shelter = 0
            WHERE 
                id = %(animal_id)s
        """

        params = {
            'animal_id': animal_id
        }
        
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
            'previous_status': previous_status,
            'status': 'Turnovered', 
            'remarks': remarks
        }

        cur.execute(sql, params)
        
        db.connection.commit()

        return cur.lastrowid

    @staticmethod
    def get_user_adoptions(user_id):
        sql = """
            SELECT 
                animal.*,
                animal.id AS id,
                user.id AS adopter_user_id,
                user.email AS adopter_email,
                user.username AS adopter_username,
                user.first_name AS adopter_first_name,
                user.last_name AS adopter_last_name,
                user.gender AS adopter_gender,
                user.photo_url AS adopter_photo_url,
                user.is_verified AS adopter_is_verified,
                user.unread_notification_count AS adopter_unread_notification_count,
                user.contact_number AS adopter_contact_number
            FROM 
                animal
            LEFT JOIN
                adoption ON animal.id = adoption.animal_id
            LEFT JOIN
                user ON adoption.user_id = user.id
            WHERE 
                user.id = %s;
        """

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        rows = cur.fetchall()
        return rows
    

    @staticmethod
    def get_applications(user_id):
        sql = """
                SELECT 
                    adoption.id as id,
                    adoption.user_id,
                    adoption.animal_id,
                    adoption.current_status,
                    adoption.interview_preference,
                    adoption.interview_preferred_date,
                    adoption.interview_preferred_time,
                    adoption.reason_to_adopt,
                    adoption.is_active,
                    adoption.zoom_url,
                    adoption.google_meet_url,
                    adoption.phone_number,                   
                    animal.name as animal_name,
                    animal.photo_url as animal_photo_url,
                    animal.is_dewormed as animal_is_dewormed,
                    animal.is_neutered as animal_is_neutered,
                    animal.in_shelter as animal_in_shelter,
                    animal.is_rescued as animal_is_rescued
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
    def get_application(application_id):
        sql = """
                SELECT 
                    adoption.id as id,
                    adoption.user_id,
                    adoption.animal_id,
                    adoption.current_status,
                    adoption.interview_preference,
                    adoption.interview_preferred_date,
                    adoption.interview_preferred_time,
                    adoption.reason_to_adopt,
                    adoption.is_active,
                    adoption.zoom_url,
                    adoption.google_meet_url,
                    adoption.phone_number,
                    animal.id as animal_id,
                    animal.name as animal_name,
                    animal.photo_url as animal_photo_url,
                    animal.is_dewormed as animal_is_dewormed,
                    animal.is_neutered as animal_is_neutered,
                    animal.in_shelter as animal_in_shelter,
                    animal.is_rescued as animal_is_rescued,
                    animal.is_adopted as animal_is_adopted,
                    animal.for_adoption as animal_for_adoption
                FROM 
                    adoption
                LEFT JOIN 
                    animal ON adoption.animal_id = animal.id
                WHERE 
                    adoption.id = %s
                    
            """        
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (application_id,))
        rows = cur.fetchone()
        return rows
    
    @staticmethod
    def get_application_history(application_id):
        sql = """
                SELECT 
                    id,
                    adoption_id,
                    previous_status,
                    status,
                    remarks,
                    created_at
                FROM 
                    adoption_status_history
                WHERE 
                    adoption_id = %s
                ORDER BY
                    created_at DESC
                    
            """        
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (application_id,))
        rows = cur.fetchall()
        return rows


    @staticmethod
    def get_for_adoptions(page_number: int, page_size: int):
        offset = (page_number - 1) * page_size

        sql = """
                SELECT 
                    animal.id as id,
                    description,
                    is_adopted,
                    name,
                    photo_url,
                    COUNT(adoption.user_id) AS application_count
                FROM animal 
                LEFT JOIN 
                    adoption ON adoption.animal_id = animal.id
                WHERE 
                    animal.is_adopted = 0 and animal.for_adoption = 1
                GROUP BY 
                    animal.id
                LIMIT %s OFFSET %s
            """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, [page_size, offset])
        data = cur.fetchall()

        sql = """
            SELECT 
                COUNT(*) as total_count
            FROM animal 
            LEFT JOIN 
                adoption ON adoption.animal_id = animal.id
            WHERE 
                animal.is_adopted = 0 and animal.for_adoption = 1
            GROUP BY 
                animal.id
        """

        cur.execute(sql)
        total_count = cur.fetchone()['total_count']
        
        return {
            'data': data,
            'total_count': total_count,
            'offset': offset
        }

    @staticmethod
    def get_animal_applications(animal_id):
        sql = """
                SELECT 
                    adoption.id as id,
                    adoption.user_id,
                    adoption.animal_id,
                    adoption.current_status,
                    adoption.interview_preference,
                    adoption.interview_preferred_date,
                    adoption.interview_preferred_time,
                    adoption.reason_to_adopt,
                    adoption.is_active,
                    adoption.zoom_url,
                    adoption.google_meet_url,
                    adoption.phone_number,
                    user.first_name,
                    user.last_name,
                    user.email,
                    user.contact_number,
                    user.photo_url,
                    animal.name as animal_name
                FROM adoption 
                LEFT JOIN 
                    user ON adoption.user_id = user.id
                LEFT JOIN
                    animal ON adoption.animal_id = animal.id
                WHERE 
                    adoption.animal_id = %s
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (animal_id,))
        rows = cur.fetchall()
        return rows
    
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
