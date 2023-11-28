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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(16) UNIQUE NOT NULL -- 'member' | 'donor' | 'volunteer' | 'adopter' | 'admin'
);

CREATE TABLE IF NOT EXISTS user_role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    role_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE IF NOT EXISTS animal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256) UNIQUE NOT NULL,
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
    for_adoption BOOLEAN NOT NULL,
    description TEXT,
    appearance TEXT,
    author_id INT NOT NULL REFERENCES user(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS adoption_application (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    animal_id INT NOT NULL,
    application_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Under Review', 'Approved', 'Rejected', 'Turnovered') DEFAULT 'Pending',
    interview_type_preference ENUM('Phone', 'Zoom', 'Google Meet') DEFAULT 'Phone',
    interview_preferred_date DATETIME NOT NULL,
    interview_preferred_time VARCHAR(256) NOT NULL,
    reason_to_adopt TEXT,
    admin_notes TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (animal_id) REFERENCES animal(id)
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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS event_pictures (
    event_id INT NOT NULL REFERENCES event(id),
    photo_url VARCHAR(256) NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (event_id, photo_url),
    CONSTRAINT unique_event_photo_url UNIQUE (event_id, photo_url)
);


CREATE TABLE IF NOT EXISTS donation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(16) NOT NULL, -- 'event' or 'org'
    user_id INT NOT NULL REFERENCES user(id),
    donation_type VARCHAR(16) NOT NULL, -- 'money' or 'in_kind'
    delivery_type VARCHAR(16), -- 'pickup' or 'deliver' (if in_kind)
    pick_up_location VARCHAR(256), -- optional, depending on delivery_type
    amount INT, -- (if money)
    remarks TEXT,
    is_confirmed BOOLEAN,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS donation_pictures (
    donation_id INT NOT NULL REFERENCES donation(id),
    photo_url VARCHAR(256) NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (donation_id, photo_url),
    CONSTRAINT unique_donation_photo_url UNIQUE (donation_id, photo_url)
);