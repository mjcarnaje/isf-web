-- Insert admin role
INSERT IGNORE INTO role (name) VALUES ('member');
INSERT IGNORE INTO role (name) VALUES ('donor');
INSERT IGNORE INTO role (name) VALUES ('volunteer');
INSERT IGNORE INTO role (name) VALUES ('admin');

-- Get the ID of the 'admin' role
SET @admin_role_id = LAST_INSERT_ID();

-- Insert user
INSERT IGNORE INTO user (email, google_id, username, first_name, last_name, password, photo_url, contact_number)
VALUES ('admin@example.com', NULL, 'admin', 'admin', 'admin', 'pbkdf2:sha256:600000$41AT9RlTuc6cKm5B$b6c91de61e1304dd5fd520c1465d097bf297441c00434ec650fed81c72013f8b', NULL, '1234567890');

-- Get the ID of the newly created user
SET @admin_user_id = LAST_INSERT_ID();

-- Associate user with admin role
INSERT IGNORE INTO user_role (user_id, role_id) VALUES (@admin_user_id, @admin_role_id);

-- Generate 10 dummy animals
INSERT IGNORE INTO animal (name, type, estimated_birth_month, estimated_birth_year, photo_url, gender, is_adopted, is_dead, is_dewormed, is_neutered, in_shelter, is_rescued, for_adoption, description, appearance, author_id)
VALUES
    ('Buddy', 'Dog', 'March', '2019', 'isf/default-dog', 'Male', 0, 0, 1, 1, 1, 0, 1, 'Buddy is a gentle and friendly dog who loves belly rubs. He has a brown and white coat and is of medium size.', 'Brown and white fur, medium size', @admin_user_id),
    ('Whiskers', 'Cat', 'July', '2020', 'isf/default-cat', 'Female', 1, 0, 1, 0, 1, 0, 1, 'Whiskers is a playful and curious cat with striking black and white fur. She enjoys playing with toys and cuddling.', 'Black and white fur, small size', @admin_user_id),
    ('Maximus', 'Dog', 'January', '2018', 'isf/default-dog', 'Male', 0, 1, 1, 1, 1, 0, 0, 'Maximus is a loyal and protective dog. He has a sleek black coat and is of large size, making him an excellent companion for walks.', 'Black fur, large size', @admin_user_id),
    ('Mittens', 'Cat', 'April', '2019', 'isf/default-cat', 'Male', 0, 0, 1, 1, 1, 0, 0, 'Mittens is a charming and laid-back cat. He has a fluffy gray and white coat, making him an ideal cuddle buddy.', 'Gray and white fur, medium size', @admin_user_id),
    ('Lola', 'Dog', 'September', '2020', 'isf/default-dog', 'Female', 1, 0, 1, 0, 1, 0, 0, 'Lola is an energetic and friendly dog who loves outdoor adventures. She has a beautiful golden coat and is of medium size.', 'Golden fur, medium size', @admin_user_id),
    ('Simba', 'Cat', 'June', '2022', 'isf/default-cat', 'Male', 0, 0, 1, 1, 1, 0, 1, 'Simba is a playful and curious kitten. With his orange tabby markings, he is sure to capture your heart with his adorable antics.', 'Orange tabby fur, small size', @admin_user_id),
    ('Sasha', 'Dog', 'December', '2017', 'isf/default-dog', 'Female', 0, 1, 1, 1, 1, 0, 0, 'Sasha is a sweet and gentle senior dog. She has a mix of black and white fur and enjoys leisurely strolls and quiet moments.', 'Black and white fur, medium size', @admin_user_id),
    ('Oliver', 'Cat', 'August', '2018', 'isf/default-cat', 'Male', 1, 0, 1, 0, 1, 0, 0, 'Oliver is a dignified and independent cat. With his sleek black coat, he exudes elegance and charm.', 'Black fur, medium size', @admin_user_id),
    ('Rosie', 'Dog', 'May', '2019', 'isf/default-dog', 'Female', 0, 0, 1, 1, 1, 0, 0, 'Rosie is a loving and loyal dog with a fluffy white coat. She enjoys cuddling on the couch and going for leisurely walks.', 'White fur, small size', @admin_user_id),
    ('Leo', 'Cat', 'October', '2021', 'isf/default-cat', 'Male', 1, 0, 1, 0, 1, 0, 0, 'Leo is a mischievous and playful cat with distinctive black and orange markings. His vibrant personality will bring joy to any home.', 'Black and orange fur, small size', @admin_user_id);

-- Generate 10 dummy events
INSERT IGNORE INTO event (name, description, cover_photo_url, start_date, end_date, location, author_id, is_done, show_in_landing)
VALUES
    ('Pet Adoption Day', 'Join us for a day filled with love and furry friends! Meet adorable cats and dogs looking for their forever homes.', 'isf/default-event', '2023-01-15 10:00:00', '2023-01-15 15:00:00', 'Local Shelter', @admin_user_id, 0, 1),
    ('Paws and Play', 'Bring your pets and let them socialize at our pet-friendly event. Enjoy games, treats, and a day of fun with fellow pet lovers.', 'isf/default-event', '2023-02-10 12:00:00', '2023-02-10 17:00:00', 'City Park', @admin_user_id, 1, 1),
    ('Feline Fiesta', 'Celebrate all things cat-related at our Feline Fiesta! Cat lovers unite for a day of catnip, toys, and adorable furry friends.', 'isf/default-event', '2023-03-20 14:00:00', '2023-03-20 19:00:00', 'Community Center', @admin_user_id, 0, 1),
    ('Canine Carnival', 'Step right up to the Canine Carnival! Enjoy games, treats, and a day filled with tail-wagging fun for dogs and their human companions.', 'isf/default-event', '2023-04-15 10:00:00', '2023-04-15 15:00:00', 'Dog Park', @admin_user_id, 0, 1),
    ('Meow Mixer', 'Calling all cat enthusiasts! Join us for the Meow Mixer, a social gathering for cat lovers. Enjoy cat-themed activities, treats, and meet adorable feline friends.', 'isf/default-event', '2023-05-10 12:00:00', '2023-05-10 17:00:00', 'Cat Cafe', @admin_user_id, 1, 1),
    ('Paws in the Park', 'Bring your furry friends to Paws in the Park, a community event filled with pet-friendly activities, live music, and a chance to connect with fellow pet owners.', 'isf/default-event', '2023-06-20 14:00:00', '2023-06-20 19:00:00', 'City Park', @admin_user_id, 0, 1),
    ('Senior Pets Day', 'Celebrate the wisdom and charm of senior pets at our Senior Pets Day. Meet older dogs and cats looking for a peaceful and loving retirement home.', 'isf/default-event', '2023-07-15 16:00:00', '2023-07-15 21:00:00', 'Senior Pet Sanctuary', @admin_user_id, 1, 0),
    ('Kitten Carnival', 'Experience the cuteness overload at the Kitten Carnival! Play with adorable kittens, enjoy carnival games, and learn about responsible kitten care.', 'isf/default-event', '2023-08-10 18:00:00', '2023-08-10 23:00:00', 'Community Center', @admin_user_id, 0, 1),
    ('Doggy Dash', 'Get ready for the Doggy Dash, a fun run for dogs and their owners! Join us for a day of fitness, prizes, and a tail-wagging good time.', 'isf/default-event', '2023-09-20 20:00:00', '2023-09-20 01:00:00', 'Dog Park', @admin_user_id, 1, 0),
    ('Purrfect Picnic', 'Enjoy a Purrfect Picnic with cats! Bring your feline friends, indulge in tasty treats, and relax in a cat-friendly outdoor setting.', 'isf/default-event', '2023-10-15 22:00:00', '2023-10-16 03:00:00', 'Cat Garden', @admin_user_id, 0, 1);

-- Insert member 1
INSERT IGNORE INTO user (email, google_id, username, first_name, last_name, password, photo_url, contact_number)
VALUES ('member1@gmail.com', NULL, 'member1', 'Member', 'One', 'pbkdf2:sha256:600000$41AT9RlTuc6cKm5B$b6c91de61e1304dd5fd520c1465d097bf297441c00434ec650fed81c72013f8b', NULL, '09999999999');

-- Get the ID of the newly created member
SET @member1_user_id = LAST_INSERT_ID();

-- Associate member 1 with 'member' role
INSERT IGNORE INTO user_role (user_id, role_id) VALUES (@member1_user_id, (SELECT id FROM role WHERE name = 'member'));

-- Insert member 2
INSERT IGNORE INTO user (email, google_id, username, first_name, last_name, password, photo_url, contact_number)
VALUES ('member2@gmail.com', NULL, 'member2', 'Member', 'Two', 'pbkdf2:sha256:600000$41AT9RlTuc6cKm5B$b6c91de61e1304dd5fd520c1465d097bf297441c00434ec650fed81c72013f8b', NULL, '09999999999');

-- Get the ID of the newly created member
SET @member2_user_id = LAST_INSERT_ID();

-- Associate member 2 with 'member' role
INSERT IGNORE INTO user_role (user_id, role_id) VALUES (@member2_user_id, (SELECT id FROM role WHERE name = 'member'));
