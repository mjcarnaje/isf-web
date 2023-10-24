from flask_login import UserMixin
from ..database import db

class Admin(UserMixin):
  def __init__(self, id, email, username, password):
    self.id = id
    self.email = email
    self.username = username
    self.password = password

  def get_id(self):
    return self.id
  
  @staticmethod
  def find_one(cls, user_id):
    sql = "SELECT * FROM admin WHERE id = %s"
    cur = db.new_cursor(dict=True)
    db.execute_sql(sql, (user_id,))
    row = cur.fetchone()
    return row
