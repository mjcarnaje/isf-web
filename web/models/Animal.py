import datetime

from ..database import db


class Animal():
    def __init__(self, name: str = None, 
                 type: str = None,
                estimated_birth_month: str = None,
                estimated_birth_year: str = None,
                photo_url: str = None,
                gender: str = None,
                is_adopted: bool = False,
                is_dead: bool = False,
                is_dewormed: bool = False,
                is_neutered: bool = False,
                in_shelter: bool = False,
                is_rescued: bool = False,
                for_adoption: bool = True,
                description: str = None,
                appearance: str = None,
                author_id: str = None,
                id: int | None = None, 
                created_at: datetime.date | None = None,
                updated_at: datetime.date | None = None,
                help_requested: bool = False
                ):
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
        self.for_adoption = for_adoption
        self.description = description
        self.appearance = appearance
        self.author_id = author_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.help_requested = help_requested

    @staticmethod
    def get_adopter(user_id: int):
        sql = """
            SELECT 
                user.id,
                user.email,
                user.username,
                user.first_name,
                user.last_name,
                user.gender,
                user.photo_url,
                user.is_verified,
                user.contact_number
            FROM 
                animal
            LEFT JOIN
                adoption ON animal.id = adoption.animal_id
            LEFT JOIN
                user ON adoption.user_id = user.id
            WHERE 
                animal.id = %s;
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (user_id,))
        row = cur.fetchone()
        return row

    @classmethod
    def find_one(cls, animal_id: int):
        sql = """
            SELECT 
                id,
                name,
                type,
                estimated_birth_month,
                estimated_birth_year,
                photo_url,
                gender,
                is_adopted,
                is_dead,
                is_dewormed,
                is_neutered,
                in_shelter,
                is_rescued,
                for_adoption,
                description,
                appearance,
                author_id,
                created_at,
                updated_at
            FROM 
                animal
            WHERE 
                animal.id = %s;
        """
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, (animal_id,))
        row = cur.fetchone()
        cur.close()
        return cls(**row)

    @staticmethod
    def insert(
        name: str, 
        type: str,
        estimated_birth_month: str,
        estimated_birth_year: str,
        photo_url: str,
        gender: str,
        is_adopted: bool,
        is_dead: bool,
        is_dewormed: bool,
        is_neutered: bool,
        is_rescued: bool,
        description: str,
        appearance: str,
        author_id: int
        ) -> int:
        sql = """
            INSERT INTO animal(
                name, type, estimated_birth_month, estimated_birth_year, photo_url, gender, is_adopted, is_dead, is_dewormed, is_neutered, is_rescued, description, appearance, author_id
            ) VALUES(%(name)s, %(type)s, %(estimated_birth_month)s, %(estimated_birth_year)s, %(photo_url)s, %(gender)s, %(is_adopted)s, %(is_dead)s, %(is_dewormed)s, %(is_neutered)s, %(is_rescued)s, %(description)s, %(appearance)s, %(author_id)s)"""
        params = {
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
            'is_rescued': is_rescued,
            'description': description,
            'appearance': appearance,
            'author_id': author_id
        }
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        db.connection.commit()
        return cur.lastrowid


    @staticmethod
    def find_all(page_number: int, page_size: int, filters: dict = None):
        offset = (page_number - 1) * page_size

        where_clauses = []
        filter_params = []

        if filters:
            for key, value in filters.items():
                if type(value) != int and not value:
                    continue

                if key == "query":
                    where_clauses.append("name LIKE %s")
                    filter_params.append(f"%{value}%")
                    continue

                where_clauses.append(f"{key} = %s")
                filter_params.append(value)

        where_clause = " AND ".join(where_clauses) if where_clauses else ""

        sql = f"""
                SELECT DISTINCT
                    id,
                    name,
                    type,
                    estimated_birth_month,
                    estimated_birth_year,
                    photo_url,
                    gender,
                    is_adopted,
                    is_dead,
                    is_dewormed,
                    is_neutered,
                    in_shelter,
                    is_rescued,
                    for_adoption,
                    description,
                    appearance,
                    author_id,
                    created_at,
                    updated_at,
                    help_requested
                FROM (
                    SELECT 
                        animal.id,
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
                        animal.for_adoption,
                        animal.description,
                        animal.appearance,
                        animal.author_id,
                        animal.created_at,
                        animal.updated_at,
                        (CASE WHEN animal_help.animal_id IS NOT NULL AND animal_help.is_fulfilled = FALSE THEN TRUE ELSE FALSE END) AS help_requested
                    FROM animal
                    LEFT JOIN animal_help ON animal_help.animal_id = animal.id
                ) AS subquery
                """

        if where_clause:
            sql += f" WHERE {where_clause}"

        count_sql = f"SELECT COUNT(*) AS total_count FROM ({sql}) AS count_subquery"
        
        sql += f" LIMIT %s OFFSET %s"
        
        cur = db.new_cursor(dictionary=True)
        cur.execute(count_sql, filter_params)
        total_count = cur.fetchone()['total_count']

        cur.execute(sql, filter_params + [page_size, offset])
        data = cur.fetchall()

        return {
            'data': data,
            'total_count': total_count,
            'offset': offset
        }


    
    @staticmethod
    def find_all_adoptions(page_number: int, page_size: int, filters: dict, user_id: str):
        offset = (page_number - 1) * page_size

        where_clauses = []
        filter_params = []

        filter_params.append(user_id)

        if filters: 
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

        sql = """
            SELECT 
                animal.*,
                IF(adoption.id IS NOT NULL, 1, 0) AS is_applied
            FROM animal
            LEFT JOIN 
                adoption ON animal.id = adoption.animal_id AND adoption.user_id = %s
            """
        
        if where_clause:
            sql += f" WHERE {where_clause}"

        sql += " LIMIT %s OFFSET %s"

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, filter_params + [page_size, offset])

        data = cur.fetchall()

        count_sql = f"""
            SELECT 
                COUNT(*) as total_count
            FROM 
                animal
            LEFT JOIN 
                adoption ON animal.id = adoption.animal_id AND adoption.user_id = %s
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
    def edit(cls, animal):
        sql = """
            UPDATE animal
            SET
                name = %(name)s,
                type = %(type)s,
                estimated_birth_month = %(estimated_birth_month)s,
                estimated_birth_year = %(estimated_birth_year)s,
                photo_url = %(photo_url)s,
                gender = %(gender)s,
                is_dead = %(is_dead)s,
                is_dewormed = %(is_dewormed)s,
                is_neutered = %(is_neutered)s,
                in_shelter = %(in_shelter)s,
                is_rescued = %(is_rescued)s,
                description = %(description)s,
                appearance = %(appearance)s,
                author_id = %(author_id)s,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                id = %(id)s
        """
        params = {
            'name': animal.name,
            'type': animal.type,
            'estimated_birth_month': animal.estimated_birth_month,
            'estimated_birth_year': animal.estimated_birth_year,
            'photo_url': animal.photo_url,
            'gender': animal.gender,
            'is_dead': animal.is_dead,
            'is_dewormed': animal.is_dewormed,
            'is_neutered': animal.is_neutered,
            'in_shelter': animal.in_shelter,
            'is_rescued': animal.is_rescued,
            'description': animal.description,
            'appearance': animal.appearance,
            'author_id': animal.author_id,
            'id': animal.id
        }
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

    @classmethod
    def get_adoption_status(cls, animal_id):
        sql = "SELECT for_adoption FROM animal WHERE id = %s"
        params = (animal_id,)

        cur = db.new_cursor()
        cur.execute(sql, params)
        
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return None


    @classmethod
    def toggle_adoption_status(cls, animal_id):
        current_status = cls.get_adoption_status(animal_id)

        new_status = 1 if current_status == 0 else 0

        sql = "UPDATE animal SET for_adoption = %s WHERE id = %s"
        params = (new_status, animal_id)

        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return new_status

    @staticmethod
    def check_if_animal_exists(event_name, id=None):
        sql = "SELECT * FROM animal WHERE name=%s"
        params = [event_name]
        if id:
            sql += " AND id != %s"
            params.append(id)
        cur = db.new_cursor(dictionary=True)
        cur.execute(sql, params)
        exists = cur.fetchone() is not None
        return exists
    
    @staticmethod
    def get_stats():
        sql = """
            SELECT
                COUNT(*) AS total_count,
                SUM(CASE WHEN type = 'cat' THEN 1 ELSE 0 END) AS cat_count,
                SUM(CASE WHEN type = 'dog' THEN 1 ELSE 0 END) AS dog_count,
                SUM(CASE WHEN is_adopted THEN 1 ELSE 0 END) AS adopted_count,
                SUM(CASE WHEN is_dead THEN 1 ELSE 0 END) AS dead_count,
                SUM(CASE WHEN is_dewormed THEN 1 ELSE 0 END) AS dewormed_count,
                SUM(CASE WHEN is_neutered THEN 1 ELSE 0 END) AS neutered_count,
                SUM(CASE WHEN in_shelter THEN 1 ELSE 0 END) AS in_shelter_count,
                SUM(CASE WHEN is_rescued THEN 1 ELSE 0 END) AS rescued_count,
                SUM(CASE WHEN for_adoption THEN 1 ELSE 0 END) AS for_adoptioncount
            FROM animal
        """

        cur = db.new_cursor(dictionary=True)
        cur.execute(sql)
        stats = cur.fetchone()

        return stats
