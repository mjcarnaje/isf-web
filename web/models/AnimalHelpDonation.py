from flask import current_app
from ..database import db

class AnimalHelpDonation:
    def __init__(
            self,
            user_id=None,
            animal_help_id=None,
            donation_type=None,
            amount=None,
            item_list=None,
            pictures=None,
            is_confirmed=None,
            is_rejected=None,
            created_at=None,
            id=None,
            user_name=None,
            user_photo_url=None,
        ):
            self.id = id
            self.user_id = user_id
            self.animal_help_id = animal_help_id
            self.donation_type = donation_type
            self.amount = amount
            self.item_list = item_list
            self.pictures = pictures
            self.is_confirmed = is_confirmed
            self.is_rejected = is_rejected
            self.created_at = created_at

            self.user_name = user_name
            self.user_photo_url = user_photo_url

    @staticmethod
    def set_to_confirmed(id):
        try:
            sql = """
                UPDATE animal_help_donation
                SET 
                    is_confirmed = 1,
                    is_rejected = 0
                WHERE id = %s
            """
            cur = db.new_cursor()
            cur.execute(sql, (id,))
            db.connection.commit()

            current_app.logger.info(f"Donation with id {id} confirmed successfully!")
        except Exception as err:
            current_app.logger.error(err)

    @staticmethod
    def set_to_rejected(id):
        try:
            sql = """
                UPDATE animal_help_donation
                SET 
                    is_rejected = 1,
                    is_confirmed = 0
                WHERE id = %s
            """
            cur = db.new_cursor()
            cur.execute(sql, (id,))
            db.connection.commit()

            current_app.logger.info(f"Donation with id {id} rejected successfully!")
        except Exception as err:
            current_app.logger.error(err)

    @staticmethod
    def set_to_pending(id):
        try:
            sql = """
                UPDATE animal_help_donation
                SET 
                    is_rejected = 0,
                    is_confirmed = 0
                WHERE id = %s
            """
            cur = db.new_cursor()
            cur.execute(sql, (id,))
            db.connection.commit()

            current_app.logger.info(f"Donation with id {id} pending successfully!")
        except Exception as err:
            current_app.logger.error(err)

    @classmethod
    def find_all_by_id(cls, animal_help_id: int):
            sql = """
                SELECT
                    donation.*,
                    CONCAT(user.first_name, ' ', user.last_name) as user_name,
                    user.photo_url as user_photo_url,
                    GROUP_CONCAT(pictures.photo_url) AS photo_urls
                FROM
                    animal_help_donation AS donation
                LEFT JOIN
                    animal_help_donation_pictures AS pictures
                ON
                    donation.id = pictures.animal_help_donation_id
                LEFT JOIN
                    user ON donation.user_id = user.id
                WHERE
                    donation.animal_help_id = %s
                GROUP BY
                    donation.id
                ORDER BY
                    created_at DESC
            """

            cur = db.new_cursor(dictionary=True)
            cur.execute(sql, (animal_help_id,))
            rows = cur.fetchall()

            donations = []
        
            for row in rows:
                photo_urls = row['photo_urls'].split(',') if row['photo_urls'] else []
                row['pictures'] = photo_urls
                del row['photo_urls']
                donations.append(cls(**row))

            return donations

    @classmethod
    def find_verified_donations(cls, animal_help_id: int):
            sql = """
                SELECT
                    donation.*,
                    CONCAT(user.first_name, ' ', user.last_name) as user_name,
                    user.photo_url as user_photo_url,
                    GROUP_CONCAT(pictures.photo_url) AS photo_urls
                FROM
                    animal_help_donation AS donation
                LEFT JOIN
                    animal_help_donation_pictures AS pictures
                ON
                    donation.id = pictures.animal_help_donation_id
                LEFT JOIN
                    user ON donation.user_id = user.id
                WHERE
                    donation.animal_help_id = %s 
                AND
                    donation.is_confirmed = 1
                GROUP BY
                    donation.id
                ORDER BY
                    created_at DESC
            """

            cur = db.new_cursor(dictionary=True)
            cur.execute(sql, (animal_help_id,))
            rows = cur.fetchall()

            donations = []
        
            for row in rows:
                photo_urls = row['photo_urls'].split(',') if row['photo_urls'] else []
                row['pictures'] = photo_urls
                del row['photo_urls']
                donations.append(cls(**row))

            return donations
    
    @classmethod
    def insert(cls, animal_help_donation):
            try:
                sql = """
                    INSERT INTO animal_help_donation (
                        user_id,
                        animal_help_id,
                        donation_type,
                        amount,
                        item_list,
                        is_confirmed
                    ) VALUES (
                        %(user_id)s,
                        %(animal_help_id)s,
                        %(donation_type)s,
                        %(amount)s,
                        %(item_list)s,
                        %(is_confirmed)s
                    )
                """
                params = {
                    'user_id': animal_help_donation.user_id,
                    'animal_help_id': animal_help_donation.animal_help_id,
                    'donation_type': animal_help_donation.donation_type,
                    'amount': animal_help_donation.amount,
                    'item_list': animal_help_donation.item_list,
                    'is_confirmed': animal_help_donation.is_confirmed,
                }

                cur = db.new_cursor()
                cur.execute(sql, params)
                db.connection.commit()

                animal_help_donation_id = cur.lastrowid

                pictures_sql = """
                    INSERT INTO animal_help_donation_pictures (
                        animal_help_donation_id, photo_url
                    ) VALUES(%s, %s)
                """

                if animal_help_donation.pictures:
                    pictures_params = [(animal_help_donation_id, photo_url) for photo_url in animal_help_donation.pictures]
                    cur.executemany(pictures_sql, pictures_params)
                
                db.connection.commit()

                current_app.logger.info("Added donation successfuly!")

                return animal_help_donation_id
            except Exception as err:
                current_app.logger.error(err)
                
