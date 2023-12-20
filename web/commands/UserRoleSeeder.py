class UserRoleSeeder:
    def __init__(self, db):
        self.db = db

    def seed(self, num_users):
        print("Seeding user role..")
        try:
            cur = self.db.connection.cursor(dictionary=True)

            sql = "SELECT role_name, user_id FROM user_role ORDER BY RAND() LIMIT 1"

            for _ in range(num_users):
                cur.execute(sql)
                result = cur.fetchone()

                if result:
                    if result['user_id'] == 1 or result['role_name'] == "Admin":
                        continue

                    print(f"Make {result['user_id']} as Member")
                    insert_sql = f"UPDATE user_role SET role_name = 'Member' WHERE user_id = {result['user_id']}"
                    cur.execute(insert_sql)

            self.db.connection.commit()
            print("User Role data seeded successfully!")
        except Exception as e:
            print(f"Error seeding user data: {str(e)}")
