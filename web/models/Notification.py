import datetime

from flask import current_app, url_for

from ..database import db
from ..enums import NotificationType
from ..utils import format_currency, pretty_date, get_image
from .NotificationSettings import NotificationSettings
from uuid import uuid4

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
        
        self.notifier_email = kwargs.get('notifier_email')
        self.notifier_username = kwargs.get('notifier_username')
        self.notifier_photo_url = kwargs.get('notifier_photo_url')
        self.notifier_first_name = kwargs.get('notifier_first_name')
        self.notifier_last_name = kwargs.get('notifier_last_name')

        self.notified_email = kwargs.get('notified_email')
        self.notified_username = kwargs.get('notified_username')
        self.notified_photo_url = kwargs.get('notified_photo_url')
        self.notified_first_name = kwargs.get('notified_first_name')
        self.notified_last_name = kwargs.get('notified_last_name')

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


    @classmethod
    def insert_multiple(cls, notifications):
        web_notifications_ids = []
        email_notifications_ids = []

        for notification in notifications:
            user_id = notification.user_to_notify_id
            notif_type = notification.type.lower()
            result = NotificationSettings.find_one(user_id=user_id)

            if result and result[f"{notif_type}_web"]:
                current_app.logger.info(f"Appending user_id ({user_id}) web notification..")
                web_notifications_ids.append(user_id)

            if result and result[f"{notif_type}_email"]:
                current_app.logger.info(f"Appending user_id ({user_id}) email notification..")
                email_notifications_ids.append(user_id)    

        sql = """
            INSERT INTO notification (
                id,
                type,
                animal_id,
                adoption_id,
                adoption_status_history_id,
                event_id,
                donation_id,
                user_who_fired_event_id,
                user_to_notify_id,
                is_archived
            ) VALUES (
                %(id)s,
                %(type)s, 
                %(animal_id)s, 
                %(adoption_id)s, 
                %(adoption_status_history_id)s, 
                %(event_id)s, 
                %(donation_id)s, 
                %(user_who_fired_event_id)s, 
                %(user_to_notify_id)s,
                %(is_archived)s
            )
        """

        cur = db.new_cursor()
        data = []

        notification_email_ids = []

        for notification in notifications:
            id = uuid4().hex
            params = {
                'id': id,
                'type': notification.type,
                'animal_id': notification.animal_id,
                'adoption_id': notification.adoption_id,
                'adoption_status_history_id': notification.adoption_status_history_id,
                'event_id': notification.event_id,
                'donation_id': notification.donation_id,
                'user_who_fired_event_id': notification.user_who_fired_event_id,
                'user_to_notify_id': notification.user_to_notify_id,
                'is_archived': notification.user_to_notify_id not in web_notifications_ids
            }
            data.append(params)
            
            if notification.user_to_notify_id in email_notifications_ids:
                notification_email_ids.append(id)

        cur.executemany(sql, data)

        sql = """
            UPDATE user
            SET 
                unread_notification_count = unread_notification_count + 1 
            WHERE id = %(user_id)s
        """

        data = []

        for notification in notifications:
            if notification.user_to_notify_id not in web_notifications_ids:
                continue
            params = {
                'user_id': notification.user_to_notify_id
            }
            data.append(params)

        cur.executemany(sql, data)

        db.connection.commit()

        from ..utils import send_notification_email

        for notification_id in notification_email_ids:
            current_app.logger.info("Sending Notification Email..")
            result = cls.find_one(notification_id=notification_id)
            send_notification_email.delay(
                subject=NotificationType[result.type].get_email_subject(), 
                recipient_email=result.notified_email, 
                title=NotificationType[result.type].get_email_title(), 
                first_name=result.notified_first_name, 
                message=result.message,
                preview_image_url=get_image(result.preview_image_url),
                sender_name=result.notifier_first_name,
                sender_email=result.notifier_email,
                button_text="",
                button_link=""
            )
        
    
    @classmethod
    def find_one(cls, notification_id: str):
        sql = """
            SELECT 
                notification.*, 
                notifier.email as notifier_email, 
                notifier.username as notifier_username, 
                notifier.first_name as notifier_first_name, 
                notifier.last_name as notifier_last_name, 
                notifier.photo_url as notifier_photo_url,
                notified.email as notified_email, 
                notified.username as notified_username, 
                notified.username as notified_username, 
                notified.first_name as notified_first_name, 
                notified.last_name as notified_last_name, 
                notified.photo_url as notified_photo_url,
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
                user as notifier ON notification.user_who_fired_event_id = notifier.id
            LEFT JOIN 
                user as notified ON notification.user_to_notify_id = notified.id
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
            WHERE
                notification.id = %(notification_id)s;
        """

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, {'notification_id': notification_id})
        row = cur.fetchone()

        if row:
            notification = cls(
                **row,
                message=cls.get_message_for_type_and_info(row['type'], row),
                redirect_url=cls.get_redirect_url(row['type'], row),
                preview_image_url=cls.get_preview_image_url(row['type'], row),
            )
            return notification
        else:
            return None

    
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
                notifier.email as notifier_email, 
                notifier.username as notifier_username, 
                notifier.first_name as notifier_first_name, 
                notifier.last_name as notifier_last_name, 
                notifier.photo_url as notifier_photo_url,
                notified.email as notified_email, 
                notified.username as notified_username, 
                notified.username as notified_username, 
                notified.first_name as notified_first_name, 
                notified.last_name as notified_last_name, 
                notified.photo_url as notified_photo_url,
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
                user as notifier ON notification.user_who_fired_event_id = notifier.id
            LEFT JOIN 
                user as notified ON notification.user_to_notify_id = notified.id
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
        full_name = f'{info["notifier_first_name"]} {info["notifier_last_name"]}'

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
                    redirect_url = url_for("admin.event.view_event", id=info['event_id'])
                else:
                    redirect_url = url_for("user.events.view_event", id=info['event_id'])
            case _:
                if is_admin:
                    redirect_url = url_for("admin.adoptions.adoption", id=info['donation_id'])
                else:
                    redirect_url = url_for("user.adoptions.adopt_me", id=info['donation_id'])        
        
        return redirect_url
