import datetime

from ..database import db


class Donation():
    def __init__(
        self, 
        type: str = None,
        user_id: int = None,
        animal_id: int = None,
        event_id: int = None,
        donation_type: str = None,
        amount: int | None = None,
        item_list: str | None = None,
        delivery_type: str = None,
        pick_up_location: str = None,
        remarks: str = None,
        thumbnail_url: str = None,
        pictures: [str] = None,
        is_confirmed: bool = False,
        created_at=None,
        id: int | None = None
    ):
        self.id = id
        self.type = type
        self.animal_id = animal_id
        self.event_id = event_id
        self.amount = amount
        self.item_list = item_list
        self.user_id = user_id
        self.donation_type = donation_type
        self.delivery_type = delivery_type
        self.pick_up_location = pick_up_location
        self.remarks = remarks
        self.thumbnail_url = thumbnail_url
        self.pictures = pictures 
        self.is_confirmed = is_confirmed
        self.created_at = created_at or datetime.datetime.now()

        
        
    @classmethod
    def find_by_id(cls, donation_id: int):
        sql = "SELECT * FROM donation WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (donation_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)    
    
    @classmethod
    def insert(cls, donation):
        sql = """
            INSERT INTO donation (
                type,
                user_id,
                donation_type,
                amount,
                item_list,
                delivery_type,
                pick_up_location,
                remarks,
                is_confirmed,
                thumbnail_url,
                created_at
            ) VALUES (
                %(type)s,
                %(user_id)s,
                %(donation_type)s,
                %(amount)s,
                %(item_list)s,
                %(delivery_type)s,
                %(pick_up_location)s,
                %(remarks)s,
                %(is_confirmed)s,
                %(thumbnail_url)s,
                %(created_at)s
            )
        """
        params = {
            'type': donation.type,
            'user_id': donation.user_id,
            'donation_type': donation.donation_type,
            'amount': donation.amount,
            'item_list': donation.item_list,
            'delivery_type': donation.delivery_type,
            'pick_up_location': donation.pick_up_location,
            'remarks': donation.remarks,
            'is_confirmed': donation.is_confirmed,
            'thumbnail_url': donation.pictures[0],
            'created_at': donation.created_at,
        }

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        donation_id = cur.lastrowid

        pictures_sql = """
            INSERT INTO donation_pictures (
                donation_id, photo_url
            ) VALUES(%s, %s)
        """

        if donation.pictures:
            pictures_params = [(donation_id, photo_url) for photo_url in donation.pictures]
            cur.executemany(pictures_sql, pictures_params)
            db.connection.commit()

        return donation_id
    
    @staticmethod
    def find_all(page_number: int, page_size: int, filters: dict = None):
        offset = (page_number - 1) * page_number
        
        where_clauses = []
        filter_params = []

        if filters: 
            for key, value in filters.items():
                if not value:
                    continue
    
                where_clauses.append(f"{key} = %s")
                filter_params.append(value)

        where_clause = " AND ".join(where_clauses) if where_clauses else ""
        
        sql = """
            SELECT 
                donation.id as id,
                donation_type,
                amount,
                item_list,
                is_confirmed,
                user.photo_url as user_photo_url,
                user.first_name as user_first_name,
                user.last_name as user_last_name
            FROM donation 
            LEFT JOIN
                user on donation.user_id = user.id
        """

        if where_clause:
            sql += f" WHERE {where_clause}"

        sql += " LIMIT %s OFFSET %s"

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, filter_params + [page_size, offset])
        data = cur.fetchall()

        count_sql = """
            SELECT 
                COUNT(*) as total_count
            FROM donation
        """

        if where_clause:
            count_sql += f" WHERE {where_clause}"

        cur.execute(count_sql, filter_params)
        total_count = cur.fetchone()['total_count']

        return {
            'data': data,
            'total_count': total_count,
            'offset': offset
        }



    @staticmethod
    def set_is_confirmed(donation_id):
        sql = """
            UPDATE donation
            SET is_confirmed = 1
            WHERE id = %s
        """

        cur_approve = db.new_cursor()
        cur_approve.execute(sql, (donation_id,))

        db.connection.commit()