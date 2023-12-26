from flask import current_app
from ..database import db

class AnimalHelp():
    def __init__(self, 
        id=None,
        animal_id=None,
        description=None,
        amount=None,
        item_list=None,
        is_fulfilled=None,
        thumbnail_url=None,
        created_at=None
        ):
        self.id = id
        self.animal_id = animal_id
        self.description = description
        self.amount = amount
        self.item_list = item_list
        self.is_fulfilled = is_fulfilled
        self.thumbnail_url = thumbnail_url
        self.created_at = created_at
    
    @staticmethod
    def set_to_fulfilled(id):
        try:
            sql = """
                UPDATE animal_help
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
    def find_one(animal_help_id):
        sql = """
            SELECT 
                animal_help.id,
                animal_help.animal_id,
                animal_help.description,
                animal_help.amount,
                animal_help.item_list,
                animal_help.is_fulfilled,
                animal_help.thumbnail_url,
                animal_help.created_at,
                animal.name AS animal_name,
                animal.description AS animal_description,
                animal.is_dewormed AS animal_is_dewormed,
                animal.is_neutered AS animal_is_neutered,
                animal.in_shelter AS animal_in_shelter,
                animal.is_rescued AS animal_is_rescued,
                animal.is_adopted AS animal_is_adopted,
                animal.photo_url as animal_photo_url
            FROM animal_help
            LEFT JOIN
                animal ON animal.id = animal_help.animal_id
            WHERE 
                animal_help.id = %(animal_help_id)s
            """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, {'animal_help_id': animal_help_id})
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
                animal_help.id,
                animal_help.animal_id,
                animal_help.description,
                animal_help.amount,
                animal_help.item_list,
                animal_help.is_fulfilled,
                animal_help.thumbnail_url,
                animal_help.created_at,
                animal.id AS animal_id,
                animal.name AS animal_name,
                animal.description AS animal_description,
                animal.is_dewormed AS animal_is_dewormed,
                animal.is_neutered AS animal_is_neutered,
                animal.in_shelter AS animal_in_shelter,
                animal.is_rescued AS animal_is_rescued,
                animal.is_adopted AS animal_is_adopted,
                animal.photo_url as animal_photo_url
            FROM animal_help
            LEFT JOIN
                animal ON animal.id = animal_help.animal_id
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
            FROM animal_help
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
    def insert(cls, animal_help):
        sql = """
            INSERT INTO animal_help (
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
            'animal_id': animal_help.animal_id,
            'description': animal_help.description,
            'amount': animal_help.amount,
            'item_list': animal_help.item_list,
            'thumbnail_url': animal_help.thumbnail_url,
        }

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.lastrowid
    
    @classmethod
    def edit(cls, animal_help):
        sql = """
            UPDATE animal_help
            SET
                description = %(description)s,
                amount = %(amount)s,
                item_list = %(item_list)s,
                thumbnail_url = %(thumbnail_url)s
            WHERE
                id = %(animal_help_id)s
        """
        params = {
            'description': animal_help.description,
            'amount': animal_help.amount,
            'item_list': animal_help.item_list,
            'thumbnail_url': animal_help.thumbnail_url,
            'animal_help_id': animal_help.id
        }
        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.rowcount

    @classmethod
    def delete(cls, animal_help_id):
        sql = "DELETE FROM animal_help WHERE id = %s"
        params = (animal_help_id,)

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.rowcount