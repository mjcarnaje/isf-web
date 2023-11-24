-- Add SQL statements to create the models
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(256) UNIQUE NOT NULL,
    google_id VARCHAR(64),
    username VARCHAR(256) NOT NULL,
    first_name VARCHAR(256) NOT NULL,
    last_name VARCHAR(256) NOT NULL,
    password VARCHAR(256) NOT NULL,
    photo_url VARCHAR(256),
    contact_number VARCHAR(12) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(16) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS user_role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    role_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE IF NOT EXISTS animal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    type VARCHAR(16) NOT NULL,
    estimated_birth_month VARCHAR(16) NOT NULL,
    estimated_birth_year VARCHAR(16) NOT NULL,
    photo_url VARCHAR(256) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    is_adopted BOOLEAN NOT NULL,
    is_dead BOOLEAN NOT NULL,
    is_dewormed BOOLEAN NOT NULL,
    is_neutered BOOLEAN NOT NULL,
    in_shelter BOOLEAN NOT NULL,
    is_rescued BOOLEAN NOT NULL,
    description TEXT,
    appearance TEXT,
    author_id INT NOT NULL REFERENCES user(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS event (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256) UNIQUE NOT NULL,
    description TEXT,
    cover_photo_url VARCHAR(256),
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    location VARCHAR(256),
    author_id INT NOT NULL REFERENCES user(id),
    is_done BOOLEAN NOT NULL,
    show_in_landing BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

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
INSERT INTO animal (name, type, estimated_birth_month, estimated_birth_year, photo_url, gender, is_adopted, is_dead, is_dewormed, is_neutered, in_shelter, is_rescued, description, appearance, author_id)
VALUES
    ('Dog1', 'Dog', 'January', '2020', 'unitrack/g4apxw3zexqjbnw1ttcu', 'Male', 0, 0, 1, 1, 1, 0, 'Friendly dog', 'Brown fur, medium size', @admin_user_id),
    ('Cat1', 'Cat', 'February', '2021', 'unitrack/g4apxw3zexqjbnw1ttcu', 'Female', 1, 0, 1, 0, 1, 0, 'Playful cat', 'Black and white, small size', @admin_user_id),
    ('Rabbit1', 'Rabbit', 'March', '2019', 'unitrack/g4apxw3zexqjbnw1ttcu', 'Male', 0, 0, 0, 1, 1, 0, 'Adorable rabbit', 'White fur, long ears', @admin_user_id),
    ('Dog2', 'Dog', 'April', '2022', 'unitrack/g4apxw3zexqjbnw1ttcu', 'Female', 0, 0, 1, 0, 0, 1, 'Energetic dog', 'Golden fur, large size', @admin_user_id),
    ('Cat2', 'Cat', 'May', '2020', 'unitrack/g4apxw3zexqjbnw1ttcu', 'Male', 1, 0, 1, 1, 1, 0, 'Independent cat', 'Gray fur, medium size', @admin_user_id),
    ('Rabbit2', 'Rabbit', 'June', '2021', 'unitrack/g4apxw3zexqjbnw1ttcu', 'Female', 0, 0, 0, 1, 0, 1, 'Curious rabbit', 'Brown fur, short ears', @admin_user_id),
    ('Dog3', 'Dog', 'July', '2018', 'unitrack/g4apxw3zexqjbnw1ttcu', 'Male', 1, 1, 1, 0, 1, 0, 'Calm dog', 'Black fur, medium size', @admin_user_id),
    ('Cat3', 'Cat', 'August', '2019', 'unitrack/g4apxw3zexqjbnw1ttcu', 'Female', 0, 1, 1, 1, 0, 1, 'Lazy cat', 'Orange fur, large size', @admin_user_id),
    ('Rabbit3', 'Rabbit', 'September', '2020', 'unitrack/g4apxw3zexqjbnw1ttcu', 'Male', 1, 0, 0, 0, 1, 0, 'Playful rabbit', 'Gray fur, floppy ears', @admin_user_id),
    ('Dog4', 'Dog', 'October', '2019', 'unitrack/g4apxw3zexqjbnw1ttcu', 'Female', 0, 0, 1, 1, 1, 1, 'Protective dog', 'White fur, small size', @admin_user_id);
