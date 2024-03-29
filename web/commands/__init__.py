from flask import Flask
from ..database.run_sql import run_sql
from ..config import Config
from ..database import db
import json
from .AnimalSeeder import AnimalSeeder
from .UserSeeder import UserSeeder
from .UserRoleSeeder import UserRoleSeeder
from .EventSeeder import EventSeeder
from .utils import get_collection_photos

def set_up_commands(app: Flask):
    @app.cli.command("reset")
    def reset_db():
        try:
            app.logger.info("Dropping Database...")
            db.execute_sql(f"DROP DATABASE IF EXISTS {Config.MYSQL_DATABASE};")
            app.logger.info("Database dropped successfully!")
            app.logger.info("---")

            app.logger.info("Creating Database...")
            db.execute_sql(f"CREATE DATABASE {Config.MYSQL_DATABASE};")
            app.logger.info("Database created successfully!")
            app.logger.info("---")

            app.logger.info("Adding tables...")
            run_sql(app, 'create-schema.sql')
            app.logger.info("Tables created successfully!")

            app.logger.info("Database reset completed!")
        except Exception as e:
            app.logger.error(f"Error during database reset: {str(e)}")

    @app.cli.command("seed")
    def seed():
        UserSeeder(db).seed(20)
        UserRoleSeeder(db).seed(10)
        AnimalSeeder(db).seed(200)
        EventSeeder(db).seed(20)
        
    @app.cli.command("save-animal-photos")
    def save_animal_photos():
        cat_photos = get_collection_photos("1973336")
        dog_photos = get_collection_photos("2109136")

        results = []

        for cat in cat_photos:
            results.append({'type': 'cat', 'link': cat})

        for dog in dog_photos:
            results.append({'type': 'dog', 'link': dog})

        with open('animal_photos.json', 'w') as outf:
            json.dump(results, outf, indent=2)

    @app.cli.command("save-user-photos")
    def save_user_photos():
        animal_photos = get_collection_photos("eR9Yy1KH53o")
        with open('user_photos.json', 'w') as outf:
            json.dump(animal_photos, outf, indent=2)

    @app.cli.command("save-event-photos")
    def save_event_photos():
        event_photos = get_collection_photos("9377028")
        with open('event_photos.json', 'w') as outf:
            json.dump(event_photos, outf, indent=2)