import datetime

from ..database import db


import datetime

class Animal():
    def __init__(self, name: str = None, type: str = None, estimated_birth_month: str = None, estimated_birth_year: str = None, photo_url: str = None, gender: str = None,
                 is_adopted: bool = False, is_dead: bool = False, is_dewormed: bool = False, is_neutered: bool = False,
                 in_shelter: bool = False, is_rescued: bool = False, description: str = None, appearance: str = None, author_id: str = None,
                 id: int | None = None, created_at: datetime.date | None = None, updated_at: datetime.date | None = None):
        self.id = id
        self.name = name
        self.type = type
        self.estimated_birth_month = estimated_birth_month
        self.estimated_birth_year = estimated_birth_year
        self.photo_url = photo_url
        self.gender = gender
        self.is_adopted = is_adopted
        self.is_dead = is_dead
        self.is_dewormed = is_dewormed
        self.is_neutered = is_neutered
        self.in_shelter = in_shelter
        self.is_rescued = is_rescued
        self.description = description
        self.appearance = appearance
        self.author_id = author_id
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def find_by_id(cls, user_id: int):
        sql = "SELECT * FROM animal WHERE id = %s"
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        return cls(**row)

    @staticmethod
    def insert(name: str, type: str, estimated_birth_month: str, estimated_birth_year: str, photo_url: str, gender: str,
            is_adopted: bool, is_dead: bool, is_dewormed: bool, is_neutered: bool,
            in_shelter: bool, is_rescued: bool, description: str, appearance: str,author_id: int) -> int:
        sql = "INSERT INTO animal (name, type, estimated_birth_month, estimated_birth_year, photo_url, gender, is_adopted, is_dead, is_dewormed, is_neutered, in_shelter, is_rescued, description, appearance, author_id) VALUES(%(name)s, %(type)s, %(estimated_birth_month)s, %(estimated_birth_year)s, %(photo_url)s, %(gender)s, %(is_adopted)s, %(is_dead)s, %(is_dewormed)s, %(is_neutered)s, %(in_shelter)s, %(is_rescued)s, %(description)s, %(appearance)s, %(author_id)s)"
        data = {
            'name': name,
            'type': type,
            'estimated_birth_month': estimated_birth_month,
            'estimated_birth_year': estimated_birth_year,
            'photo_url': photo_url,
            'gender': gender,
            'is_adopted': is_adopted,
            'is_dead': is_dead,
            'is_dewormed': is_dewormed,
            'is_neutered': is_neutered,
            'in_shelter': in_shelter,
            'is_rescued': is_rescued,
            'description': description,
            'appearance': appearance,
            'author_id': author_id
        }
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, data)
        db.connection.commit()
        return cur.lastrowid


    @staticmethod
    def find_all(page_number: int, page_size: int, query: str =  None):
        offset = (page_number - 1) * page_size

        where_clause = ""
        filter_params = []
        
        if query:
            where_clause += " AND name LIKE %s"
            filter_params.append(f"%{query}%")

        sql = f"""
            SELECT * FROM animal
            """
        if where_clause: 
            sql += f" WHERE {where_clause}"
        sql += " LIMIT %s OFFSET %s"

        cur = db.new_cursor(dictionary=True)

        cur.execute(sql, filter_params + [page_size, offset])

        data = cur.fetchall()

        count_sql = f"SELECT COUNT(*) FROM animal"

        if where_clause: 
            count_sql += f" WHERE {where_clause}"

        cur.execute(count_sql, filter_params)
        total_count = cur.fetchone()['COUNT(*)']

        has_previous_page = offset > 0
        has_next_page = (offset + page_size) < total_count

        return {
            'data': data,
            'has_previous_page': has_previous_page,
            'has_next_page': has_next_page,
            'total_count': total_count
        }
    @classmethod
    def edit(cls, animal):
        sql = """
            UPDATE animal
            SET
                name = %s,
                type = %s,
                estimated_birth_month = %s,
                estimated_birth_year = %s,
                photo_url = %s,
                gender = %s,
                is_adopted = %s,
                is_dead = %s,
                is_dewormed = %s,
                is_neutered = %s,
                in_shelter = %s,
                is_rescued = %s,
                description = %s,
                appearance = %s,
                author_id = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                id = %s
        """
        params = (
            animal.name,
            animal.type,
            animal.estimated_birth_month,
            animal.estimated_birth_year,
            animal.photo_url,
            animal.gender,
            animal.is_adopted,
            animal.is_dead,
            animal.is_dewormed,
            animal.is_neutered,
            animal.in_shelter,
            animal.is_rescued,
            animal.description,
            animal.appearance,
            animal.author_id,
            animal.id
        )
        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.rowcount
    
    @classmethod
    def delete(cls, animal_id):
        sql = "DELETE FROM animal WHERE id = %s"
        params = (animal_id,)

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.rowcount