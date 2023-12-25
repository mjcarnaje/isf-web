from ..database import db

class EventPost:
    def __init__(
        self,
        user_id=None,
        event_id=None,
        post_text=None,
        pictures=None,
        created_at=None,
        id=None,
        user_name=None,
        user_photo_url=None
    ):
        self.user_id = user_id
        self.event_id = event_id
        self.post_text = post_text
        self.pictures = pictures
        self.created_at = created_at
        self.id = id,
        self.user_name=user_name
        self.user_photo_url=user_photo_url

    @classmethod
    def insert(cls, event_post):
        sql = """
            INSERT INTO event_post (
                user_id,
                event_id,
                post_text
            ) VALUES (
                %(user_id)s,
                %(event_id)s,
                %(post_text)s
            )
        """
        params = {
            'user_id': event_post.user_id,
            'event_id': event_post.event_id,
            'post_text': event_post.post_text
        }

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        event_post_id = cur.lastrowid

        pictures_sql = """
            INSERT INTO event_post_pictures (
                event_post_id, photo_url
            ) VALUES(%s, %s)
        """

        if event_post.pictures:
            pictures_params = [(event_post_id, photo_url) for photo_url in event_post.pictures]
            cur.executemany(pictures_sql, pictures_params)
            db.connection.commit()

        return event_post_id
        
    @classmethod
    def find_posts(cls, event_id):
        sql = """
            SELECT
                event_post.*,
                CONCAT(user.first_name, ' ', user.last_name) as user_name,
                user.photo_url as user_photo_url,
                GROUP_CONCAT(pictures.photo_url) AS photo_urls
            FROM
                event_post
            LEFT JOIN
                event_post_pictures AS pictures
            ON
                event_post.id = pictures.event_post_id
            LEFT JOIN
                user ON event_post.user_id = user.id
            WHERE
                event_post.event_id = %s
            GROUP BY
                event_post.id
            ORDER BY
                created_at DESC
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (event_id,))
        rows = cur.fetchall()

        updates = []
        for row in rows:
            photo_urls = row['photo_urls'].split(',') if row['photo_urls'] else []
            row['pictures'] = photo_urls
            del row['photo_urls']
            updates.append(cls(**row))

        return updates

    @staticmethod
    def delete(post_id):
        sql = """
            DELETE
                FROM event_post
            WHERE
                id = %(post_id)s
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, { 'post_id': post_id })
        db.connection.commit()
        

