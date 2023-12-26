from flask import current_app
from ..database import db

class AnimalHelpPost:
    def __init__(
        self,
        user_id=None,
        animal_help_id=None,
        post_text=None,
        created_at=None,
        pictures=None,
        id=None,
        user_name=None,
        user_photo_url=None,
    ):
        self.id = id
        self.user_id = user_id
        self.animal_help_id = animal_help_id
        self.post_text = post_text
        self.pictures = pictures
        self.created_at = created_at

        self.user_name = user_name
        self.user_photo_url = user_photo_url

    @classmethod
    def find_one(cls, update_id: int):
        sql = "SELECT * FROM animal_help_post WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (update_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)

    @classmethod
    def insert(cls, update):
        sql = """
            INSERT INTO animal_help_post (
                animal_help_id,
                post_text,
                user_id
            ) VALUES (
                %(animal_help_id)s,
                %(post_text)s,
                %(user_id)s
            )
        """
        params = {
            'animal_help_id': update.animal_help_id,
            'post_text': update.post_text,
            'user_id': update.user_id,
        }

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        update_id = cur.lastrowid

        pictures_sql = """
            INSERT INTO animal_help_post_pictures (
                animal_help_post_id,
                photo_url
            ) VALUES (%s, %s)
        """

        if update.pictures:
            pictures_params = [(update_id, photo_url) for photo_url in update.pictures]
            cur.executemany(pictures_sql, pictures_params)
            db.connection.commit()
        
        current_app.logger.info("Added post successfully!")

        return update_id
    
    @staticmethod
    def delete(post_id):
        sql = """
            DELETE 
                FROM animal_help_post
            WHERE
                id = %(post_id)s
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, { 'post_id': post_id })
        db.connection.commit()
        

    
    @classmethod
    def find_all_by_id(cls, animal_help_id):
        sql = """
            SELECT
                post.*,
                post.id as id,
                CONCAT(user.first_name, ' ', user.last_name) as user_name,
                user.photo_url as user_photo_url,
                GROUP_CONCAT(pictures.photo_url) AS photo_urls
            FROM
                animal_help_post AS post
            LEFT JOIN
                animal_help_post_pictures AS pictures
            ON
                post.id = pictures.animal_help_post_id
            LEFT JOIN
                user ON post.user_id = user.id
            WHERE
                post.animal_help_id = %s
            GROUP BY
                post.id
            ORDER BY
                created_at DESC
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (animal_help_id,))
        rows = cur.fetchall()

        updates = []
        for row in rows:
            photo_urls = row['photo_urls'].split(',') if row['photo_urls'] else []
            row['pictures'] = photo_urls
            del row['photo_urls']
            updates.append(cls(**row))

        return updates
