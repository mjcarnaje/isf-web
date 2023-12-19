from ..database import db
from ..utils import pagination

class Event():
    def __init__(
            self, 
            id=None, 
            name=None, 
            description=None, 
            cover_photo_url=None, 
            start_date=None, 
            end_date=None, 
            location=None, 
            author_id=None, 
            status=None,
            is_cancelled=None,
            who_can_see_it=None,
            who_can_join=None,
            created_at=None, 
            updated_at=None
        ):
        self.id = id
        self.name = name
        self.description = description
        self.cover_photo_url = cover_photo_url
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.author_id = author_id
        self.status = status
        self.is_cancelled = is_cancelled
        self.who_can_see_it = who_can_see_it
        self.who_can_join = who_can_join
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get_featured():
        sql = """
            SELECT
                id,
                name,
                description,
                cover_photo_url,
                start_date,
                end_date,
                location,
                who_can_see_it,
                who_can_join,
                is_cancelled,
                author_id,
                created_at,
                updated_at,
                CASE
                    WHEN is_cancelled = true THEN 'Cancelled'
                    WHEN start_date > NOW() THEN 'Scheduled'
                    WHEN start_date <= NOW() AND end_date >= NOW() THEN 'In Progress'
                    WHEN end_date < NOW() THEN 'Completed'
                END AS status
            FROM 
                event
            WHERE
                start_date <= NOW()
                AND end_date >= NOW()
                AND is_cancelled != true
            ORDER BY
                start_date DESC
            LIMIT 3
        """

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql)
        featured_data = cur.fetchall()

        return featured_data


    @staticmethod
    def find_all(page_number: int, page_size: int, filters: dict = None):
        offset = (page_number - 1) * page_size

        where_clauses = []
        filter_params = []
        
        for key, value in filters.items():
            if not value:
                continue

            if key == "query":
                where_clauses.append("name LIKE %s")
                filter_params.append(f"%{value}%")
                continue

            where_clauses.append(f"{key} = %s")
            filter_params.append(value)

        where_clause = " AND ".join(where_clauses) if where_clauses else ""

        count_sql = """
            SELECT COUNT(*) AS total_count
            FROM (
                SELECT
                    name,
                    who_can_see_it,
                    CASE
                        WHEN is_cancelled = true THEN 'Cancelled'
                        WHEN start_date > NOW() THEN 'Scheduled'
                        WHEN start_date <= NOW() AND end_date >= NOW() THEN 'In Progress'
                        WHEN end_date < NOW() THEN 'Completed'
                    END AS status
                FROM 
                    event
            ) AS subquery
        """

        if where_clause:
            count_sql += f" WHERE {where_clause}"

        cur = db.new_cursor(dictionary=True)
        cur.execute(count_sql, filter_params)
        total_count = cur.fetchone()["total_count"]

        sql = """
            SELECT *
            FROM (
                SELECT
                    id,
                    name,
                    description,
                    cover_photo_url,
                    start_date,
                    end_date,
                    location,
                    who_can_see_it,
                    who_can_join,
                    is_cancelled,
                    author_id,
                    created_at,
                    updated_at,
                    CASE
                        WHEN is_cancelled = true THEN 'Cancelled'
                        WHEN start_date > NOW() THEN 'Scheduled'
                        WHEN start_date <= NOW() AND end_date >= NOW() THEN 'In Progress'
                        WHEN end_date < NOW() THEN 'Completed'
                    END AS status
                FROM 
                    event
                ORDER BY
                    start_date DESC
            ) AS subquery
        """


        if where_clause:
            sql += f" WHERE {where_clause}"

        sql += " LIMIT %s OFFSET %s"

        cur.execute(sql, filter_params + [page_size, offset])
        data = cur.fetchall()

        return {
            'data': data,
            'total_count': total_count,
            'offset': offset
        }

    @classmethod
    def find_by_id(cls, event_id):
        sql = """
                SELECT
                    id,
                    name,
                    description,
                    cover_photo_url,
                    start_date,
                    end_date,
                    location,
                    who_can_see_it,
                    who_can_join,
                    is_cancelled,
                    author_id,
                    created_at,
                    updated_at,
                    CASE
                        WHEN is_cancelled = true THEN 'Cancelled'
                        WHEN start_date > NOW() THEN 'Scheduled'
                        WHEN start_date <= NOW() AND end_date >= NOW() THEN 'In Progress'
                        WHEN end_date < NOW() THEN 'Completed'
                    END AS status
                FROM 
                    event
                WHERE id = %s
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (event_id,))
        row = cur.fetchone()

        if not row:
            return None
        return cls(**row)

    @staticmethod
    def get_statistics(event_id):
        sql = """
             SELECT
                COUNT(*) AS invited_count,
                SUM(CASE WHEN status = 'Maybe' THEN 1 ELSE 0 END) AS maybe_count,
                SUM(CASE WHEN status = 'Going' THEN 1 ELSE 0 END) AS going_count,
                SUM(CASE WHEN status = 'Cannot Go' THEN 1 ELSE 0 END) AS cant_go_count
            FROM event_volunteer
            WHERE 
                event_id = %(event_id)s
        """

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, {
            'event_id': event_id
        })
        stats = cur.fetchone()

        return stats
    
    @staticmethod
    def get_volunteers(event_id):
        sql = """
            SELECT 
                status,
                user.photo_url as photo_url,
                COALESCE(user.first_name, ' ', user.last_name) as name
            FROM event_volunteer
            LEFT JOIN
                user ON user.id = event_volunteer.volunteer_id
            WHERE 
                event_id = %(event_id)s
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, {
            'event_id': event_id
        })
        data = cur.fetchall()
        print(data)
        return data


    
    @staticmethod
    def get_invitation(event_id, user_id):
        sql = """
                SELECT 
                    status
                FROM event_volunteer 
                WHERE event_id = %(event_id)s and volunteer_id = %(user_id)s
            """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, {
            'event_id': event_id,
            'user_id': user_id
        })
        row = cur.fetchone()
        return row

    @staticmethod
    def update_status(event_id, user_id, status):
        sql = """
            UPDATE event_volunteer 
            SET
                status = %(status)s
            WHERE 
                event_id = %(event_id)s and volunteer_id = %(user_id)s
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, {
            'event_id': event_id,
            'user_id': user_id,
            'status': status
        })
        db.connection.commit()


    @classmethod
    def insert(cls, event):
        sql = """
            INSERT INTO event (
                name, 
                description, 
                cover_photo_url, 
                start_date, 
                end_date, 
                location, 
                who_can_see_it,
                who_can_join,
                author_id
            ) 
            VALUES (
                %(name)s, 
                %(description)s,
                %(cover_photo_url)s,
                %(start_date)s,
                %(end_date)s,
                %(location)s,
                %(who_can_see_it)s,
                %(who_can_join)s,
                %(author_id)s
            )
        """
        params = {
            'name': event.name,
            'description': event.description,
            'cover_photo_url': event.cover_photo_url,
            'start_date': event.start_date,
            'end_date': event.end_date,
            'location': event.location,
            'who_can_see_it': event.who_can_see_it,
            'who_can_join': event.who_can_join,
            'author_id': event.author_id,
        }

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()
        
        event_id = cur.lastrowid

        return event_id
    
    @staticmethod
    def invite_users(event_id: int, user_ids: [int]):
        sql = """
            INSERT INTO event_volunteer (
            event_id,  volunteer_id
            ) VALUES (%(event_id)s, %(volunteer_id)s)
        """

        cur = db.new_cursor()

        data = [
            {
                'event_id': event_id,
                'volunteer_id': user_id
            } for user_id in user_ids
        ]

        cur.executemany(sql, data)
        
        db.connection.commit()


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
                who_can_see_it = %s,
                who_can_join = %s,
                author_id = %s,
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
            event.who_can_see_it,
            event.who_can_join,
            event.author_id,
            event.id
        )
        cur = db.new_cursor()
        cur.execute(sql, params)
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
    
    @classmethod
    def cancel(cls, event_id):
        sql = "UPDATE event SET is_cancelled = 1 WHERE id = %s"
        params = (event_id,)

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.rowcount
    