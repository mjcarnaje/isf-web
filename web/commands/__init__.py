from flask import Flask
from ..database.run_sql import run_sql
from ..config import Config
from ..database import db


def set_up_commands(app: Flask):
  @app.cli.command("reset-tables")
  def reset_tables():
      try:
          app.logger.info("Running reseting tables...")
          run_sql(app, 'create-schema.sql')
          app.logger.info("Tables created successfully!")

          app.logger.info("Reset tables completed!")
      except Exception as e:
          app.logger.error(f"Error during database reset: {str(e)}")

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

          app.logger.info("Seeding data...")
          run_sql(app, 'seed.sql')
          app.logger.info("Seeding completed successfully!")

          app.logger.info("Database reset completed!")
      except Exception as e:
          app.logger.error(f"Error during database reset: {str(e)}")

