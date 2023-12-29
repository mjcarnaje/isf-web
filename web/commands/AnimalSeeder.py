import random
import json
from faker import Faker

class AnimalSeeder:
    def __init__(self, db):
        self.fake = Faker()
        self.animal_photos_copy = self.load_animal_photos()
        self.db = db

    def load_animal_photos(self):
        with open('animal_photos.json', 'r') as json_file:
            animal_photos = json.load(json_file)
            random.shuffle(animal_photos)
        return animal_photos.copy()

    def generate_random_date(self):
        return self.fake.date_between(start_date='-5y', end_date='today')

    def generate_random_gender(self):
        return random.choice(['Male', 'Female'])

    def generate_fake_description(self, animal_type):
        return self.fake.sentence(nb_words=10) + f' {animal_type}.'

    def generate_fake_appearance(self, animal_type):
        return self.fake.sentence(nb_words=6) + f' {animal_type}.'

    def generate_fake_sql_values(self, animal_type, is_adopted, is_dead, is_dewormed, is_neutered, in_shelter, is_rescued, for_adoption):
        if not self.animal_photos_copy:
            self.animal_photos_copy = self.load_animal_photos()

        photo_url = self.animal_photos_copy.pop(0)

        return (
            "('{}', "
            "'{}', "
            "'{}', "
            "'{}', "
            "'{}', "
            "'{}', "
            "{}, {}, {}, {}, {}, {}, {}, "
            "'{}', "
            "'{}', "
            "'{}')".format(
                self.fake.first_name(),
                animal_type,
                self.generate_random_date().strftime('%B'),
                self.generate_random_date().strftime('%Y'),
                photo_url,
                self.generate_random_gender(),
                is_adopted, is_dead, is_dewormed, is_neutered, in_shelter, is_rescued, for_adoption,
                self.generate_fake_description(animal_type),
                self.generate_fake_appearance(animal_type),
                1
            )
        )

    def seed(self, num_animals):
        sql_statements = []

        for index in range(num_animals):
            is_adopted = random.choice([0, 1])

            animal_data = (
                random.choice(['Dog', 'Cat']),
                is_adopted,
                random.choice([0, 1]),
                random.choice([0, 1]),
                random.choice([0, 1]),
                random.choice([0, 1]),
                random.choice([0, 1]),
                0 if is_adopted else random.choice([0, 1, 1, 1]),
            )
            sql_values = self.generate_fake_sql_values(*animal_data)
            sql_statements.append(sql_values)
            print(f"Seeding animal {index}")

        sql = (
            "INSERT IGNORE INTO animal (name, type, estimated_birth_month, estimated_birth_year, "
            "photo_url, gender, is_adopted, is_dead, is_dewormed, is_neutered, in_shelter, is_rescued, "
            "for_adoption, description, appearance, author_id) VALUES\n" +
            ',\n'.join(sql_statements) +
            ";"
        )

        try:
            cur = self.db.connection.cursor()
            cur.execute(sql)
            self.db.connection.commit()
            print("Animal data seeded successfully!")
        except Exception as e:
            print(f"Error seeding animal data: {str(e)}")

