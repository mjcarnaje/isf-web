from flask import current_app

from ..database import db


class Donation():
    def __init__(
        self, 
        id: int | None = None,
        type: str = None,
        user_id: int = None,
        animal_help_id: int = None,
        donation_type: str = None,
        amount: int | None = None,
        delivery_type: str = None,
        pick_up_location: str = None,
        item_list: str | None = None,
        remarks: str = None,
        status: str = None,
        thumbnail_url: str = None,
        pictures: [str] = None,
        created_at=None,

        user_photo_url: str | None = None,
        user_first_name: str | None = None,
        user_last_name: str | None = None,
    ):
        self.id = id
        self.type = type
        self.user_id = user_id
        self.animal_help_id = animal_help_id
        self.amount = amount
        self.item_list = item_list
        self.donation_type = donation_type
        self.delivery_type = delivery_type
        self.pick_up_location = pick_up_location
        self.remarks = remarks
        self.pictures = pictures 
        self.status = status
        self.thumbnail_url = thumbnail_url
        self.created_at = created_at

        self.user_photo_url = user_photo_url
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name

        
    @classmethod
    def find_one(cls, donation_id: int):
        sql = """
            SELECT 
                donation.id,
                donation.type,
                donation.user_id,
                donation.animal_help_id,
                donation.donation_type,
                donation.amount,
                donation.delivery_type,
                donation.pick_up_location,
                donation.item_list,
                donation.remarks,
                donation.status, 
                donation.thumbnail_url, 
                donation.created_at, 
                GROUP_CONCAT(donation_pictures.photo_url) AS photo_urls,
                user.photo_url as user_photo_url,
                user.first_name as user_first_name,
                user.last_name as user_last_name
            FROM donation 
            LEFT JOIN
                donation_pictures on donation.id = donation_pictures.donation_id
            LEFT JOIN
                user on donation.user_id = user.id
            GROUP BY
                donation.id
            WHERE
                donation.id = %s
        """
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
                animal_help_id,
                donation_type,
                amount,
                item_list,
                delivery_type,
                pick_up_location,
                remarks,
                thumbnail_url
            ) VALUES (
                %(type)s,
                %(user_id)s,
                %(animal_help_id)s,
                %(donation_type)s,
                %(amount)s,
                %(item_list)s,
                %(delivery_type)s,
                %(pick_up_location)s,
                %(remarks)s,
                %(thumbnail_url)s
            )
        """
        params = {
            'type': donation.type,
            'user_id': donation.user_id,
            'animal_help_id': donation.animal_help_id,
            'donation_type': donation.donation_type,
            'amount': donation.amount,
            'item_list': donation.item_list,
            'delivery_type': donation.delivery_type,
            'pick_up_location': donation.pick_up_location,
            'remarks': donation.remarks,
            'thumbnail_url': donation.pictures[0],
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
    
    @classmethod
    def find_all(cls, page_number: int, page_size: int, filters: dict = None):
        offset = (page_number - 1) * page_size
        
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
                donation.id,
                donation.type,
                donation.user_id,
                donation.animal_help_id,
                donation.donation_type,
                donation.amount,
                donation.delivery_type,
                donation.pick_up_location,
                donation.item_list,
                donation.remarks,
                donation.status,
                donation.thumbnail_url,
                donation.created_at, 
                GROUP_CONCAT(donation_pictures.photo_url) AS photo_urls,
                user.photo_url as user_photo_url,
                user.first_name as user_first_name,
                user.last_name as user_last_name
            FROM donation 
            LEFT JOIN
                donation_pictures on donation.id = donation_pictures.donation_id
            LEFT JOIN
                user on donation.user_id = user.id
        """

        if where_clause:
            sql += f" WHERE {where_clause}"

        sql += """ 
                GROUP BY
                    donation.id
                LIMIT %s OFFSET %s
            """

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, filter_params + [page_size, offset])
        rows = cur.fetchall()

        donations = []

        for row in rows:
            photo_urls = row['photo_urls'].split(',') if row['photo_urls'] else []
            row['pictures'] = photo_urls
            del row['photo_urls']
            donations.append(cls(**row))

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
            'data': donations,
            'total_count': total_count,
            'offset': offset
        }


    @staticmethod
    def set_to_confirmed(id):
        try:
            sql = """
                UPDATE donation
                SET 
                    status = 'Confirmed'
                WHERE id = %(id)s
            """

            params = {
                'id': id
            }
            
            cur = db.new_cursor()
            cur.execute(sql, params)

            sql = """
                INSERT INTO donation_status_history (
                    donation_id,
                    new_status
                )
                VALUES (
                    %(donation_id)s,
                    %(new_status)s
                )
            """

            params = {
                'donation_id': id,
                'new_status': 'Confirmed', 
            }

            cur.execute(sql, params)
                
            db.connection.commit()

            current_app.logger.info(f"Donation with id {id} confirmed successfully!")

            return cur.lastrowid
        except Exception as err:
            current_app.logger.error(err)

    @staticmethod
    def set_to_rejected(id):
        try:
            sql = """
                UPDATE donation
                SET 
                    status = 'Rejected'
                WHERE id = %(id)s
            """

            params = {
                'id': id
            }
            
            cur = db.new_cursor()
            cur.execute(sql, params)

            sql = """
                INSERT INTO donation_status_history (
                    donation_id,
                    new_status
                )
                VALUES (
                    %(donation_id)s,
                    %(new_status)s
                )
            """

            params = {
                'donation_id': id,
                'new_status': 'Rejected', 
            }

            cur.execute(sql, params)
                
            db.connection.commit()
            
            current_app.logger.info(f"Donation with id {id} rejected successfully!")

            return cur.lastrowid
        except Exception as err:
            current_app.logger.error(err)

    @staticmethod
    def set_to_pending(id):
        try:
            sql = """
                UPDATE donation
                SET 
                    status = 'Pending'
                WHERE id = %(id)s
            """

            params = {
                'id': id
            }
            
            cur = db.new_cursor()
            cur.execute(sql, params)

            sql = """
                INSERT INTO donation_status_history (
                    donation_id,
                    new_status
                )
                VALUES (
                    %(donation_id)s,
                    %(new_status)s
                )
            """

            params = {
                'donation_id': id,
                'new_status': 'Rejected', 
            }

            cur.execute(sql, params)
                
            db.connection.commit()
            
            current_app.logger.info(f"Donation with id {id} pending successfully!")

            return cur.lastrowid
        except Exception as err:
            current_app.logger.error(err)