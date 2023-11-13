import os

from flask import Flask

from ..database import db

script_path = os.path.join(os.path.dirname(
    __file__), 'create_tables_script.sql')


def create_tables(app: Flask):
    with open(script_path, 'r') as f:
        sql = f.read()
        with app.app_context():
            sql = sql.split(';')
            sql.pop()
            cur = db.connection.cursor()
            for statement in sql:
                cur.execute(statement)
                db.connection.commit()
