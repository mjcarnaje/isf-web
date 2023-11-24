from ..database import db

class Event():
    def __init__(self, id=None, name=None, description=None, cover_photo_url=None, start_date=None, end_date=None, location=None, author_id=None, is_done=None, show_in_landing=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.cover_photo_url = cover_photo_url
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.author_id = author_id
        self.is_done = is_done
        self.show_in_landing = show_in_landing
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def find_by_id(cls, event_id):
        sql = "SELECT * FROM event WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (event_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)

    @classmethod
    def insert(cls, event):
        sql = """
            INSERT INTO event (
                name, description, cover_photo_url, start_date, end_date, location, author_id, is_done, show_in_landing
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            event.name,
            event.description,
            event.cover_photo_url,
            event.start_date,
            event.end_date,
            event.location,
            event.author_id,
            event.is_done,
            event.show_in_landing,
        )

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.lastrowid

    @staticmethod
    def check_if_event_exists(event_name, id=None):
        sql = "SELECT * FROM event WHERE name=%s"
        params = [event_name]
        if id:
            sql += " AND id != %s"
            params.append(id)
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        exists = cur.fetchone() is not None
        return exists
