
import random
import json
from faker import Faker
from werkzeug.security import generate_password_hash
import string

class UserSeeder:
    def __init__(self, db):
        self.fake = Faker()
        self.user_photos_copy = self.load_user_photos()
        self.db = db

    def load_user_photos(self):
        with open('user_photos.json', 'r') as json_file:
            user_photos = json.load(json_file)
            random.shuffle(user_photos)
        return user_photos.copy()

    def generate_random_string(self, length):
        return ''.join(random.choices(string.digits, k=length))

    def generate_fake_sql_values(self):
        if not self.user_photos_copy:
            self.user_photos_copy = self.load_user_photos()

        photo_url = self.user_photos_copy.pop(0)
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        user_name = f"{first_name.lower()}_{last_name.lower()}"
        email = f"{user_name}@gmail.com"

        return (
            "('{}', "  # email
            "'{}', "  # google_id
            "'{}', "  # username
            "'{}', "  # first_name
            "'{}', "  # last_name
            "'{}', "  # gender
            "'{}', "  # password
            "'{}', "  # photo_url
            "'{}', "  # is_verified
            "'{}', "  # contact_number
            "'{}')"   # created_at
            .format(
                email,
                self.fake.uuid4(),
                user_name,
                first_name,
                last_name,
                random.choice(['Male', 'Female', 'Other']),
                generate_password_hash(user_name),  # Assuming you have a generate_password_hash function
                photo_url,
                1,
                self.generate_random_string(12),
                self.fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            )
        )

    def seed(self, num_users):
        sql_statements = []

        for index in range(num_users):
            user_values = self.generate_fake_sql_values()
            sql_statements.append(user_values)
            print(f"Seeding user {index}")

        sql = (
            "INSERT IGNORE INTO user (email, google_id, username, first_name, last_name, gender, " +
            "password, photo_url, is_verified, contact_number, created_at) VALUES\n" +
            ',\n'.join(sql_statements) +
            ";"
        )

        try:
            cur = self.db.connection.cursor()
            cur.execute(sql)
            self.db.connection.commit()
            print("User data seeded successfully!")
        except Exception as e:
            print(f"Error seeding user data: {str(e)}")
