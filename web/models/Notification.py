import datetime

from flask import url_for

from ..database import db
from ..enums import NotificationType
from ..socket import socketio
from ..utils import format_currency, pretty_date


class Notification:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.type = kwargs.get('type')
        self.animal_id = kwargs.get('animal_id')
        self.adoption_id = kwargs.get('adoption_id')
        self.adoption_status_history_id = kwargs.get('adoption_status_history_id')
        self.event_id = kwargs.get('event_id')
        self.donation_id = kwargs.get('donation_id')
        self.user_who_fired_event_id = kwargs.get('user_who_fired_event_id')
        self.user_to_notify_id = kwargs.get('user_to_notify_id')
        self.is_read = kwargs.get('is_read', False)
        self.is_archived = kwargs.get('is_archived', False)

        self.message = kwargs.get('message')
        self.redirect_url = kwargs.get('redirect_url')
        
        self.user_username = kwargs.get('user_username')
        self.first_name = kwargs.get('user_first_name')
        self.last_name = kwargs.get('user_last_name')
        self.user_photo_url = kwargs.get('user_photo_url')

        self.preview_image_url = kwargs.get('preview_image_url')

        self.animal_name = kwargs.get('animal_name')
        self.animal_photo_url = kwargs.get('animal_photo_url')
        
        self.adoption_status = kwargs.get('adoption_status')
        self.adoption_interview_preference = kwargs.get('adoption_interview_preference')
        self.previous_status = kwargs.get('previous_status')
        
        self.donation_amount = kwargs.get('donation_amount')
        self.donation_item_list = kwargs.get('donation_item_list')
        self.donation_thumbnail_url = kwargs.get('donation_thumbnail_url')

        self.event_name = kwargs.get('event_name')
        self.event_cover_photo = kwargs.get('event_cover_photo')

        self.created_at = pretty_date(kwargs.get('created_at', datetime.datetime.now()))
        self.updated_at = pretty_date(kwargs.get('updated_at', datetime.datetime.now()))
        
    @classmethod
    def increment_count(notification):
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
    def mark_as_archived(cls, notification_id, user_id):
        notification_sql = """
            UPDATE notification
            SET 
                is_archived = 1,
                is_read = 1
            WHERE user_to_notify_id=%(user_id)s and id=%(notification_id)s
        """

        params = {
            'user_id': user_id,
            'notification_id': notification_id
        }

        cur = db.new_cursor(dictionary=True)
        cur.execute(notification_sql, params)

        db.connection.commit()


    @staticmethod
    def insert_multiple(notifications):
        sql = """
            INSERT INTO notification (
                type,
                animal_id,
                adoption_id,
                adoption_status_history_id,
                event_id,
                donation_id,
                user_who_fired_event_id,
                user_to_notify_id
            ) VALUES (
                %(type)s, 
                %(animal_id)s, 
                %(adoption_id)s, 
                %(adoption_status_history_id)s, 
                %(event_id)s, 
                %(donation_id)s, 
                %(user_who_fired_event_id)s, 
                %(user_to_notify_id)s
            )
        """

        cur = db.new_cursor()

        data = []

        for notification in notifications:
            params = {
                'type': notification.type,
                'animal_id': notification.animal_id,
                'adoption_id': notification.adoption_id,
                'adoption_status_history_id': notification.adoption_status_history_id,
                'event_id': notification.event_id,
                'donation_id': notification.donation_id,
                'user_who_fired_event_id': notification.user_who_fired_event_id,
                'user_to_notify_id': notification.user_to_notify_id
            }
            data.append(params)

        cur.executemany(sql, data)

        sql = """
            UPDATE user
            SET 
                unread_notification_count = unread_notification_count + 1 
            WHERE id = %(user_id)s
        """

        data = []

        for notification in notifications:
            params = {
                'user_id': notification.user_to_notify_id
            }
            data.append(params)

        cur.executemany(sql, data)
        
        db.connection.commit()

        socketio.emit("notification")


    @classmethod
    def find_all(cls, page_number: int, page_size: int, filters: dict = None):
        offset = (page_number - 1) * page_size

        where_clauses = []
        filter_params = []

        for key, value in filters.items():
            if value == "" or value is None:
                continue

            where_clauses.append(f"{key} = %s")
            filter_params.append(value)

        where_clause = " AND ".join(where_clauses) if where_clauses else ""
        
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
                donation.amount as donation_amount,
                donation.item_list as donation_item_list,
                donation.thumbnail_url as donation_thumbnail_url,
                event.name as event_name,
                event.cover_photo_url as event_cover_photo_url
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
            LEFT JOIN 
                event ON notification.event_id = event.id
        """

        if where_clause:
            sql += f" WHERE {where_clause}"

        sql += f""" 
            ORDER BY 
                notification.created_at DESC
            LIMIT %s OFFSET %s
        """


        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, filter_params + [page_size, offset])
        rows = cur.fetchall()

        notifications = [
            cls(
                **row,
                message=cls.get_message_for_type_and_info(row['type'], row),
                redirect_url=cls.get_redirect_url(row['type'], row),
                preview_image_url=cls.get_preview_image_url(row['type'], row),
            ) for row in rows
    ]

        return notifications
    
    @staticmethod
    def get_preview_image_url(notification_type, info):
        image_url = ""

        match notification_type:
            case NotificationType.ADOPTION_REQUEST.value:
                image_url = info['animal_photo_url']
            case NotificationType.ADOPTION_STATUS_UPDATE.value:
                image_url = ''
            case NotificationType.ADD_DONATION_MONEY.value:
                image_url = info['donation_thumbnail_url']
            case NotificationType.ADD_DONATION_IN_KIND.value:
                image_url = info['donation_thumbnail_url']
            case NotificationType.DONATION_STATUS_UPDATE.value:
                image_url = ''
            case NotificationType.EVENT_INVITED.value:
                image_url = info['event_cover_photo_url']
            case _:
                image_url = ''
                
        return image_url

    @staticmethod
    def get_message_for_type_and_info(notification_type, info):
        full_name = f'{info["user_first_name"]} {info["user_last_name"]}'

        message = ""

        match notification_type:
            case NotificationType.ADOPTION_REQUEST.value:
                message += f'{full_name} has requested to adopt {info["animal_name"]}.'
            case NotificationType.ADOPTION_STATUS_UPDATE.value:
                message += f'The status of your adoption application is now {info["adoption_status"]} (previously {info["previous_status"]}).'
                if info['adoption_status'] == "Interview":
                    if info['adoption_interview_preference'] == "Zoom" or info['adoption_interview_preference'] == "Google Meet":
                        message += f" Please check the {info['adoption_interview_preference']} link and save it for the interview date and time."
                    else:
                        message += f" Check your phone the admin might call you!."
            case NotificationType.ADD_DONATION_MONEY.value:
                message += f"{full_name} has donated money amount of {format_currency(info['donation_amount'])}"
            case NotificationType.ADD_DONATION_IN_KIND.value:
                message += f"{full_name} has donated {info['donation_item_list']}."
            case NotificationType.DONATION_STATUS_UPDATE.value:
                message += "Donate updated"
            case NotificationType.EVENT_INVITED.value:
                message += f"You have been invited to {info['event_name']}"
            case _:
                message += "Unkown message"
        
        return message


    @staticmethod
    def get_redirect_url(notification_type, info):
        is_admin = info['user_to_notify_id'] == 1

        redirect_url = ""

        match notification_type:
            case NotificationType.ADOPTION_REQUEST.value:
                if is_admin:
                    redirect_url = url_for("admin.adoptions.adoption", id=info['animal_id'])
                else:
                    redirect_url = url_for("user.adoptions.adopt_me", id=info['animal_id'])
            case NotificationType.ADOPTION_STATUS_UPDATE.value:
                if is_admin:
                    redirect_url = url_for("admin.adoptions.adoption", id=info['animal_id'])
                else:
                    redirect_url = url_for("user.adoptions.adopt_me", id=info['animal_id'])
                
            case NotificationType.ADD_DONATION_MONEY.value:
                if is_admin:
                    redirect_url = url_for("admin.adoptions.adoption", id=info['donation_id'])
                else:
                    redirect_url = url_for("user.adoptions.adopt_me", id=info['donation_id'])
            case NotificationType.ADD_DONATION_IN_KIND.value:
                if is_admin:
                    redirect_url = url_for("admin.adoptions.adoption", id=info['donation_id'])
                else:
                    redirect_url = url_for("user.adoptions.adopt_me", id=info['donation_id'])
            case NotificationType.DONATION_STATUS_UPDATE.value:
                if is_admin:
                    redirect_url = url_for("admin.adoptions.adoption", id=info['donation_id'])
                else:
                    redirect_url = url_for("user.adoptions.adopt_me", id=info['donation_id'])
            case NotificationType.EVENT_INVITED.value:
                if is_admin:
                    redirect_url = url_for("admin.events.view_event", id=info['event_id'])
                else:
                    redirect_url = url_for("user.events.view_event", id=info['event_id'])
            case _:
                if is_admin:
                    redirect_url = url_for("admin.adoptions.adoption", id=info['donation_id'])
                else:
                    redirect_url = url_for("user.adoptions.adopt_me", id=info['donation_id'])        
        
        return redirect_url
