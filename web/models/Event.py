from ..database import db
import datetime

class Event():
    def __init__(self, id=None, name=None, description=None, cover_photo_url=None, start_date=None, end_date=None, location=None, author_id=None, is_done=None, show_in_landing=None, pictures:[str] = [], created_at=None, updated_at=None,):
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
        self.pictures = pictures
        self.created_at = created_at
        self.updated_at = updated_at
        

    @staticmethod
    def find_all(show_landing_page_only: bool = False):
        sql = "SELECT * FROM event"
        
        if show_landing_page_only:
            sql += " WHERE show_in_landing = 1"

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql)
        
        data = cur.fetchall()
        
        return {
            'data': data
        }
    
    @classmethod
    def find_by_id(cls, event_id):
        sql = "SELECT * FROM event WHERE id = %s"
        picture_sql = "SELECT photo_url FROM event_pictures WHERE event_id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (event_id,))
        row = cur.fetchone()

        cur.execute(picture_sql, (event_id,))
        pictures = [row['photo_url'] for row in cur.fetchall()]
        row['pictures'] = pictures
        
        if not row:
            return None
        print(row)
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
        
        event_id = cur.lastrowid
        
        pictures_sql = """
            INSERT INTO event_pictures (
                event_id, photo_url
            ) VALUES(%s, %s)
        """

        if event.pictures:
            pictures_params = [(event_id, photo_url) for photo_url in event.pictures]
            cur.executemany(pictures_sql, pictures_params)
            db.connection.commit()

        return event_id

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
    
    @classmethod
    def edit(cls, event):
        sql = """
            UPDATE event
            SET
                name = %s,
                description = %s,
                cover_photo_url = %s,
                start_date = %s,
                end_date = %s,
                location = %s,
                author_id = %s,
                is_done = %s,
                show_in_landing = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                id = %s
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
            event.id
        )
        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        # Insert new pictures
        pictures_sql = """
            INSERT IGNORE INTO event_pictures (
                event_id, photo_url
            ) VALUES(%s, %s)
        """

        if event.pictures:
            pictures_params = [(event.id, photo_url) for photo_url in event.pictures]
            cur.executemany(pictures_sql, pictures_params)
            db.connection.commit()

        return event.id
    
    @classmethod
    def delete(cls, event_id):
        sql = "DELETE FROM event WHERE id = %s"
        params = (event_id,)

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.rowcount