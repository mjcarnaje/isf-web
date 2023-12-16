from ..database import db

class NotificationSettings:
    DEFAULT_SETTINGS = {
        'user_email': '',
        'user_first_name': '',
        
        'adoption_request_web': True,
        'adoption_status_update_web': True,
        'add_donation_money_web': True,
        'add_donation_in_kind_web': True,
        'donation_status_update_web': True,
        'event_invited_web': True,
        
        'adoption_request_email': True,
        'adoption_status_update_email': True,
        'add_donation_money_email': True,
        'add_donation_in_kind_email': True,
        'donation_status_update_email': True,
        'event_invited_email': True,
    }

    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        for setting, default_value in self.DEFAULT_SETTINGS.items():
            setattr(self, setting.upper(), kwargs.get(setting, default_value))

    @staticmethod
    def find_one(user_id):
        cur = db.new_cursor(dictionary=True)
        cur.execute("""
            SELECT 
                notification_settings.*, 
                user.email as user_email,
                user.first_name as user_first_name
            FROM notification_settings
            LEFT JOIN user ON user.id = notification_settings.user_id 
            WHERE notification_settings.user_id = %(user_id)s
        """, {'user_id': user_id})
        result = cur.fetchone()
        return result

    @classmethod
    def insert_default(cls, user_id):
        cur = db.new_cursor(dictionary=True)
        cur.execute("""
            INSERT INTO notification_settings 
            (user_id, adoption_request_web, adoption_status_update_web, add_donation_money_web, add_donation_in_kind_web, 
             donation_status_update_web, event_invited_web, adoption_request_email, adoption_status_update_email, 
             add_donation_money_email, add_donation_in_kind_email, donation_status_update_email, event_invited_email)
            VALUES (%(user_id)s, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        """, {'user_id': user_id})
        db.connection.commit()

    @classmethod
    def update_notification_settings(cls, user_id, **kwargs):
        try:
            cur = db.new_cursor(dictionary=True)
            update_query = """
                UPDATE notification_settings 
                SET {}
                WHERE user_id = %(user_id)s
            """.format(', '.join([f'{key} = %({key})s' for key in kwargs.keys()]))
            cur.execute(update_query, {'user_id': user_id, **kwargs})
            db.connection.commit()
        except Exception as error:
            print(error)

    @classmethod
    def create_from_db_result(cls, result):
        return cls(
            user_id=result['user_id'],
            adoption_request_web=bool(result['adoption_request_web']),
            adoption_status_update_web=bool(result['adoption_status_update_web']),
            add_donation_money_web=bool(result['add_donation_money_web']),
            add_donation_in_kind_web=bool(result['add_donation_in_kind_web']),
            donation_status_update_web=bool(result['donation_status_update_web']),
            event_invited_web=bool(result['event_invited_web']),
            
            adoption_request_email=bool(result['adoption_request_email']),
            adoption_status_update_email=bool(result['adoption_status_update_email']),
            add_donation_money_email=bool(result['add_donation_money_email']),
            add_donation_in_kind_email=bool(result['add_donation_in_kind_email']),
            donation_status_update_email=bool(result['donation_status_update_email']),
            event_invited_email=bool(result['event_invited_email'])
        )
