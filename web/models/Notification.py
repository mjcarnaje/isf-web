import datetime
from flask import url_for

from ..database import db

from ..utils import pretty_date

class Notification:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.type = kwargs.get('type')
        self.animal_id = kwargs.get('animal_id')
        self.adoption_id = kwargs.get('adoption_id')
        self.adoption_status_history_id = kwargs.get('adoption_status_history_id')
        self.donation_id = kwargs.get('donation_id')
        self.user_who_fired_event_id = kwargs.get('user_who_fired_event_id')
        self.user_to_notify_id = kwargs.get('user_to_notify_id')
        self.is_read = kwargs.get('is_read', False)

        self.message = kwargs.get('message')
        self.redirect_url = kwargs.get('redirect_url')
        
        self.user_username = kwargs.get('user_username')
        self.first_name = kwargs.get('user_first_name')
        self.last_name = kwargs.get('user_last_name')
        self.user_photo_url = kwargs.get('user_photo_url')

        self.animal_name = kwargs.get('animal_name')
        self.animal_photo_url = kwargs.get('animal_photo_url')

        self.adoption_status = kwargs.get('adoption_status')
        self.adoption_interview_preference = kwargs.get('adoption_interview_preference')
        self.previous_status = kwargs.get('previous_status')
        
        self.donation_amount = kwargs.get('donation_amount')

        self.created_at = pretty_date(kwargs.get('created_at', datetime.datetime.now()))
        self.updated_at = pretty_date(kwargs.get('updated_at', datetime.datetime.now()))
        
    @classmethod
    def increment_count(cls, notification):
        sql = """
            UPDATE user
            SET unread_notification_count = unread_notification_count + 1 
            WHERE id = %(user_id)s
        """
        params = {
            'user_id': notification.user_to_notify_id
        }

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

    @classmethod
    def mark_all_as_read(cls, user_id):
        user_sql = """
            UPDATE user
            SET unread_notification_count = 0
            WHERE id = %(user_id)s
        """

        params = {
            'user_id': user_id
        }

        cur = db.new_cursor(dictionary=True)
        cur.execute(user_sql, params)

        notification_sql = """
            UPDATE notification
            SET is_read = 1
            WHERE user_to_notify_id = %(user_id)s and is_read = 0
        """
        
        cur.execute(notification_sql, params)

        db.connection.commit()

    @classmethod
    def mark_as_read(cls, notification_id, user_id):
        user_sql = """
            UPDATE user
            SET unread_notification_count = GREATEST(unread_notification_count - 1, 0)
            WHERE id = %(user_id)s
        """

        params = {
            'user_id': user_id
        }

        cur = db.new_cursor(dictionary=True)
        cur.execute(user_sql, params)

        params['notification_id'] = notification_id

        notification_sql = """
            UPDATE notification
            SET is_read = 1
            WHERE user_to_notify_id = %(user_id)s and id = %(notification_id)s
        """
        
        cur.execute(notification_sql, params)

        db.connection.commit()

    @classmethod
    def insert(clc, notification):
        sql = """
            INSERT INTO notification (
                type,
                animal_id,
                adoption_id,
                adoption_status_history_id,
                donation_id,
                user_who_fired_event_id,
                user_to_notify_id
            ) VALUES (
                %(type)s, 
                %(animal_id)s, 
                %(adoption_id)s, 
                %(adoption_status_history_id)s, 
                %(donation_id)s, 
                %(user_who_fired_event_id)s, 
                %(user_to_notify_id)s
            )
        """
        
        params = {
            'type': notification.type,
            'animal_id': notification.animal_id,
            'adoption_id': notification.adoption_id,
            'adoption_status_history_id': notification.adoption_status_history_id,
            'donation_id': notification.donation_id,
            'user_who_fired_event_id': notification.user_who_fired_event_id,
            'user_to_notify_id': notification.user_to_notify_id
        }

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()


    @classmethod
    def get_notifications(cls, user_id, limit=None):
        sql = f"""
            SELECT 
                notification.*, 
                user.username as user_username, 
                user.first_name as user_first_name, 
                user.last_name as user_last_name, 
                user.photo_url as user_photo_url,
                animal.name as animal_name,
                animal.photo_url as animal_photo_url,
                adoption_status_history.previous_status as previous_status, 
                adoption_status_history.status as adoption_status, 
                adoption.interview_preference as adoption_interview_preference, 
                donation.amount as donation_amount
            FROM 
                notification
            LEFT JOIN 
                user ON notification.user_who_fired_event_id = user.id
            LEFT JOIN 
                animal ON notification.animal_id = animal.id
            LEFT JOIN
                adoption ON notification.adoption_id = adoption.id
            LEFT JOIN 
                adoption_status_history ON notification.adoption_status_history_id = adoption_status_history.id
            LEFT JOIN 
                donation ON notification.donation_id = donation.id
            WHERE 
                notification.user_to_notify_id = %(user_id)s
            ORDER BY 
                notification.created_at DESC
        """
        sql += f" LIMIT {limit}" if limit else ""

        params = {'user_id': user_id}

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        rows = cur.fetchall()

        notifications = [
            cls(
                **row,
                message=cls.get_message_for_type_and_info(row['type'], row),
                redirect_url=cls.get_redirect_url(row['type'], row),
            ) for row in rows
        ]

        return notifications

    @staticmethod
    def get_message_for_type_and_info(notification_type, info):
        message_templates = {
            'ADOPTION_REQUEST': f'{info["user_first_name"]} {info["user_last_name"]} has requested to adopt {info["animal_name"]}.',
            'ADOPTION_STATUS_UPDATE': f'The status of your adoption application is now {info["adoption_status"]} (previously {info["previous_status"]}).',
            'ADD_DONATION': f'A new donation of {info["donation_amount"]} has been added.',
            'DONATION_STATUS_UPDATE': 'The status of your donation has been updated.',
        }

        base_message = message_templates.get(notification_type, 'Unknown notification type.')

        if notification_type == 'ADOPTION_STATUS_UPDATE' and info['adoption_status'] == "Interview":
            if info['adoption_interview_preference'] == "Zoom" or info['adoption_interview_preference'] == "Google Meet":
                base_message += f" Please check the {info['adoption_interview_preference']} link and save it for the interview date and time."
            else:
                base_message += f" Check your phone the admin might call you!."

        return base_message


    @staticmethod
    def get_redirect_url(notification_type, info):
        is_admin = info['user_to_notify_id'] == 1
        redirect_url_templates = {
            'ADOPTION_REQUEST': 'admin.adoptions.adoption' if is_admin else 'user.adoptions.adopt_me',
            'ADOPTION_STATUS_UPDATE': 'admin.adoptions.adoption' if is_admin else 'user.adoptions.adopt_me',
            'ADD_DONATION': 'admin.animals.adopt' if is_admin else 'user.adoptions.adopt_me',
            'DONATION_STATUS_UPDATE': 'admin.animals.adopt' if is_admin else 'user.adoptions.adopt_me',
        }
        id_key = 'animal_id' if notification_type in {'ADOPTION_REQUEST', 'ADOPTION_STATUS_UPDATE'} else 'donation_id'
        return url_for(redirect_url_templates.get(notification_type, 'Unknown notification type.'), id=info[id_key])