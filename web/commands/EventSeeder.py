
import random
import json
from faker import Faker
import string

class EventSeeder:
    def __init__(self, db):
        self.fake = Faker()
        self.event_photos_copy = self.load_user_photos()
        self.db = db

    def load_user_photos(self):
        with open('event_photos.json', 'r') as json_file:
            event_photos = json.load(json_file)
            random.shuffle(event_photos)
        return event_photos.copy()

    def generate_random_string(self, length):
        return ''.join(random.choices(string.digits, k=length))

    def generate_fake_sql_values(self):
        if not self.event_photos_copy:
            self.event_photos_copy = self.load_user_photos()

        photo_url = self.event_photos_copy.pop(0)

        return (
            "('{}', "  # index 0: name
            "'{}', "   # index 1: description
            "'{}', "   # index 2: cover_photo_url
            "'{}', "   # index 3: start_date
            "'{}', "   # index 4: end_date
            "'{}', "   # index 5: location
            "'{}', "   # index 6: who_can_see_it
            "'{}', "   # index 7: is_cancelled
            "'{}', "   # index 8: 1
            "'{}') "   # index 9: created_at
            .format(
                self.fake.name(),  # 0
                self.fake.text(),  # 1
                photo_url,         # 2
                self.fake.date_time_between(start_date='-5y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),  # 3
                self.fake.date_time_between(start_date='-5y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),  # 4
                self.fake.city(),
                self.fake.random_element(elements=('Public', 'Verified Users', 'Member-Only')),  # 5
                random.choice([0, 0, 0, 1]),  # 6
                1,  # 7
                self.fake.date_time_between(start_date='-5y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),  # 8
            )
        )


    def seed(self, num_users):
        sql_statements = []

        for index in range(num_users):
            user_values = self.generate_fake_sql_values()
            sql_statements.append(user_values)
            print(f"Seeding event {index}")

        sql = (
            "INSERT IGNORE INTO event (name, description, cover_photo_url, start_date, end_date, location, " +
            "who_can_see_it, is_cancelled, author_id, created_at) VALUES\n" +
            ',\n'.join(sql_statements) +
            ";"
        )

        try:
            cur = self.db.connection.cursor()
            cur.execute(sql)
            self.db.connection.commit()
            print("Event data seeded successfully!")
        except Exception as e:
            print(f"Error seeding user data: {str(e)}")
