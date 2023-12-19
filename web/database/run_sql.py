import os

from flask import Flask

from ..database import db

def run_sql(app: Flask, file_name: str):
    s_path = os.path.join(os.path.dirname(__file__), 'scripts', file_name)
    
    with open(s_path, 'r') as f:
        sql = f.read()
        with app.app_context():
            sql = sql.split('--;;;;--')
            sql.pop()
            cur = db.connection.cursor()
            for statement in sql:
                print(statement)
                cur.execute(statement)
                db.connection.commit()
