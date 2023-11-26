import datetime

from ..database import db


class Donation():
    def __init__(self, type: str = None,  user_id: int = None, donation_type: str = None, amount: int | None = None, delivery_type: str = None, pick_up_location: str = None, remarks: str = None, pictures: [str] = None, is_confirmed: bool = False, created_at: datetime.datetime = None, id: int | None = None):
        self.id = id
        self.type = type
        self.amount = amount
        self.user_id = user_id
        self.donation_type = donation_type
        self.delivery_type = delivery_type
        self.pick_up_location = pick_up_location
        self.remarks = remarks
        self.pictures = pictures 
        self.is_confirmed = is_confirmed
        self.created_at = created_at
        
        
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
        donation_sql = """
            INSERT INTO donation (
                type, user_id, donation_type, amount, delivery_type, pick_up_location, remarks, is_confirmed, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        donation_params = (
            donation.type,
            donation.user_id,
            donation.donation_type,
            donation.amount,
            donation.delivery_type,
            donation.pick_up_location,
            donation.remarks,
            donation.is_confirmed,
            donation.created_at,
        )

        cur = db.new_cursor()
        cur.execute(donation_sql, donation_params)
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
    def get_user_donations(user_id):
        donation_sql = """
            SELECT * FROM donation WHERE user_id = %s ORDER BY created_at DESC
        """

        picture_sql = """
            SELECT photo_url FROM donation_pictures WHERE donation_id = %s
        """

        cur = db.new_cursor(dictionary=True)
        cur.execute(donation_sql, (user_id,))
        donations = cur.fetchall()

        for donation in donations:
            donation_id = donation['id']
            cur.execute(picture_sql, (donation_id,))
            pictures = [row['photo_url'] for row in cur.fetchall()]
            donation['pictures'] = pictures

        return [Donation(**donation) for donation in donations]
    
    @staticmethod
    def get_donations():
        donation_sql = """
            SELECT * FROM donation ORDER BY created_at DESC
        """

        picture_sql = """
            SELECT photo_url FROM donation_pictures WHERE donation_id = %s
        """

        cur = db.new_cursor(dictionary=True)
        cur.execute(donation_sql)
        donations = cur.fetchall()

        for donation in donations:
            donation_id = donation['id']
            cur.execute(picture_sql, (donation_id,))
            pictures = [row['photo_url'] for row in cur.fetchall()]
            donation['pictures'] = pictures

        return [Donation(**donation) for donation in donations]

