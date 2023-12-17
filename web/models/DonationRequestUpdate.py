from flask import current_app
from ..database import db

class DonationRequestUpdate():
    def __init__(
        self,
        user_id=None,
        donation_request_id=None,
        update_text=None,
        created_at=None,
        pictures=None,
        id=None,
        user_name=None,
        user_photo_url=None,
    ):
        self.id = id
        self.user_id = user_id
        self.donation_request_id = donation_request_id
        self.update_text = update_text
        self.pictures = pictures
        self.created_at = created_at

        self.user_name = user_name
        self.user_photo_url = user_photo_url

    @classmethod
    def find_by_id(cls, update_id: int):
        sql = "SELECT * FROM donation_request_update WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (update_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)

    @classmethod
    def insert(cls, update):
        sql = """
            INSERT INTO donation_request_update (
                donation_request_id,
                update_text,
                user_id
            ) VALUES (
                %(donation_request_id)s,
                %(update_text)s,
                %(user_id)s
            )
        """
        params = {
            'donation_request_id': update.donation_request_id,
            'update_text': update.update_text,
            'user_id': update.user_id,
        }

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        update_id = cur.lastrowid

        pictures_sql = """
            INSERT INTO donation_request_update_pictures (
                donation_request_update_id,
                photo_url
            ) VALUES (%s, %s)
        """

        if update.pictures:
            pictures_params = [(update_id, photo_url) for photo_url in update.pictures]
            cur.executemany(pictures_sql, pictures_params)
            db.connection.commit()
        
        current_app.logger.info("Added post successfully!")

        return update_id
    
    @classmethod
    def find_all_by_id(cls, donation_request_id):
        sql = """
            SELECT
                post.*,
                CONCAT(user.first_name, ' ', user.last_name) as user_name,
                user.photo_url as user_photo_url,
                GROUP_CONCAT(pictures.photo_url) AS photo_urls
            FROM
                donation_request_update AS post
            LEFT JOIN
                donation_request_update_pictures AS pictures
            ON
                post.id = pictures.donation_request_update_id
            LEFT JOIN
                user ON post.user_id = user.id
            WHERE
                post.donation_request_id = %s
            GROUP BY
                post.id
            ORDER BY
                created_at DESC
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (donation_request_id,))
        rows = cur.fetchall()

        updates = []
        for row in rows:
            photo_urls = row['photo_urls'].split(',') if row['photo_urls'] else []
            row['pictures'] = photo_urls
            del row['photo_urls']
            updates.append(cls(**row))

        return updates
