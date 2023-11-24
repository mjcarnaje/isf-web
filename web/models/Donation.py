import datetime

from ..database import db

class Donation():
    def __init__(self, type: str = None,  user_id: int = None, donation_type: str = None, delivery_type: str = None, pick_up_location: str = None, description: str = None, evidence_pictures: str = None, is_confirmed: bool = False, created_at: datetime.datetime = None, id: int | None = None):
        self.id = id
        self.type = type
        self.user_id = user_id
        self.donation_type = donation_type
        self.delivery_type = delivery_type
        self.pick_up_location = pick_up_location
        self.description = description
        self.evidence_pictures = evidence_pictures 
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
        sql = """
            INSERT INTO donation (
                type, user_id, donation_type, delivery_type, pick_up_location, description, evidence_pictures, is_confirmed
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            donation.type,
            donation.user_id,
            donation.donation_type,
            donation.delivery_type,
            donation.pick_up_location,
            donation.description,
            donation.evidence_pictures,
            donation.is_confirmed,
        )
        cur = db.new_cursor()
        cur.execute(sql, params)
        db.connection.commit()

        return cur.lastrowid