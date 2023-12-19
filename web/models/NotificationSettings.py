from ..database import db

class NotificationSettings:
    DEFAULT_SETTINGS = {
        'user_id': '',

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
                *
            FROM notification_settings
            WHERE notification_settings.user_id = %(user_id)s
        """, {'user_id': user_id})
        result = cur.fetchone()
        return result

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