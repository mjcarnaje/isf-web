from flask import current_app
from ..database import db
from .Animal import Animal

class AskForHelp():
    def __init__(self, 
        id=None,
        animal_id=None,
        description=None,
        amount=None,
        item_list=None,
        pictures= None,
        is_fulfilled=None,
        created_at=None,
        ):
        self.id = id
        self.animal_id = animal_id
        self.description = description
        self.amount = amount
        self.item_list = item_list
        self.is_fulfilled = is_fulfilled
        self.created_at = created_at
        self.pictures = pictures
    
    @staticmethod
    def set_to_fulfilled(id):
        try:
            sql = """
                UPDATE donation_request
                SET is_fulfilled = 1
                WHERE id = %s
            """
            cur = db.new_cursor()
            cur.execute(sql, (id,))
            db.connection.commit()

            current_app.logger.info(f"Donation request with id {id} confirmed successfully!")
        except Exception as err:
            current_app.logger.error(err)

    @staticmethod
    def find_one(request_id):
        sql = """
            SELECT 
                *,
                donation_request.id as id,
                donation_request.description as description,
                animal.id AS animal_id,
                animal.name AS animal_name,
                animal.photo_url as animal_photo_url
            FROM donation_request
            LEFT JOIN
                animal ON animal.id = donation_request.animal_id
            WHERE 
                donation_request.id = %(request_id)s
            """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, {
            'request_id': request_id,
        })
        data = cur.fetchone()
        return data 

    @staticmethod
    def find_all(page_number: int, page_size: int, filters: dict = None):
        offset = (page_number - 1) * page_size

        where_clauses = []
        filter_params = []

        if filters:
            for key, value in filters.items():
                if not value:
                    continue

                if key == "query":
                    where_clauses.append("description LIKE %s")
                    filter_params.append(f"%{value}%")
                else:
                    where_clauses.append(f"{key} = %s")
                    filter_params.append(value)

        where_clause = " AND ".join(where_clauses) if where_clauses else ""

        sql = f"""
            SELECT 
                *,
                donation_request.id as id,
                animal.id AS animal_id,
                donation_request.description as description,
                animal.name AS animal_name,
                animal.photo_url as animal_photo_url
            FROM donation_request
            LEFT JOIN
                animal ON animal.id = donation_request.animal_id
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
            FROM donation_request
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


    @classmethod
    def insert(cls, donation_request):
        sql = """
            INSERT INTO donation_request (
                animal_id,
                description,
                amount,
                item_list,
                thumbnail_url
            ) VALUES (
                %(animal_id)s,
                %(description)s,
                %(amount)s,
                %(item_list)s,
                %(thumbnail_url)s
            )
        """
        params = {
            'animal_id': donation_request.animal_id,
            'description': donation_request.description,
            'amount': donation_request.amount,
            'item_list': donation_request.item_list,
            'thumbnail_url': donation_request.pictures[0],
        }

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        donation_request_id = cur.lastrowid

        pictures_sql = """
            INSERT INTO donation_request_pictures (
                donation_request_id, photo_url
            ) VALUES(%s, %s)
        """

        if donation_request.pictures:
            pictures_params = [(donation_request_id, photo_url) for photo_url in donation_request.pictures]
            cur.executemany(pictures_sql, pictures_params)
            db.connection.commit()

        return donation_request_id
    
    @classmethod
    def edit(cls, animal):
        pass

    @classmethod
    def delete(cls, animal_id):
        pass

    @staticmethod
    def find_animals_options():
        filters = {
            'is_adopted': False,
            'is_dead': False
        }
        results = Animal.find_all(page_number=1, page_size=12, filters=filters)
        return results['data']