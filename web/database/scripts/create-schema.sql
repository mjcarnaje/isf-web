CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(256) UNIQUE NOT NULL,
    google_id VARCHAR(64),
    username VARCHAR(256) NOT NULL,
    first_name VARCHAR(256) NOT NULL,
    last_name VARCHAR(256) NOT NULL,
    password VARCHAR(256) NOT NULL,
    photo_url VARCHAR(256),
    is_verified BOOLEAN DEFAULT 0,
    unread_notification_count INT DEFAULT 0,
    contact_number VARCHAR(12) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notification_settings (
    user_id INT PRIMARY KEY,
    
    adoption_request_web BOOLEAN DEFAULT 1,
    adoption_status_update_web BOOLEAN DEFAULT 1,
    add_donation_money_web BOOLEAN DEFAULT 1,
    add_donation_in_kind_web BOOLEAN DEFAULT 1,
    donation_status_update_web BOOLEAN DEFAULT 1,
    event_invited_web BOOLEAN DEFAULT 1,

    adoption_request_email BOOLEAN DEFAULT 1,
    adoption_status_update_email BOOLEAN DEFAULT 1,
    add_donation_money_email BOOLEAN DEFAULT 1,
    add_donation_in_kind_email BOOLEAN DEFAULT 1,
    donation_status_update_email BOOLEAN DEFAULT 1,
    event_invited_email BOOLEAN DEFAULT 1,
    
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS role (
    name ENUM('Admin', 'Member', 'Non-Member') DEFAULT 'Member' PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS user_role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    role_name ENUM('Admin', 'Member', 'Non-Member'),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (role_name) REFERENCES role(name)
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

CREATE TABLE IF NOT EXISTS adoption (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    animal_id INT NOT NULL,
    current_status ENUM('Pending', 'Interview', 'Approved', 'Rejected', 'Turnovered') DEFAULT 'Pending',
    interview_preference ENUM('Phone', 'Zoom', 'Google Meet') DEFAULT 'Phone',
    interview_preferred_date DATETIME NOT NULL,
    interview_preferred_time VARCHAR(256) NOT NULL,
    reason_to_adopt TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    zoom_url TEXT, 
    google_meet_url TEXT,
    phone_number VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (animal_id) REFERENCES animal(id)
);

CREATE TABLE IF NOT EXISTS adoption_status_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    adoption_id INT NOT NULL,
    previous_status ENUM('Pending', 'Interview', 'Approved', 'Rejected', 'Turnovered') NOT NULL,
    status ENUM('Pending', 'Interview', 'Approved', 'Rejected', 'Turnovered') NOT NULL,
    remarks TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (adoption_id) REFERENCES adoption(id)
);

CREATE TABLE IF NOT EXISTS event (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256) UNIQUE NOT NULL,
    description TEXT,
    cover_photo_url VARCHAR(256),
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    location VARCHAR(256),
    who_can_see_it ENUM('Public', 'Verified User') DEFAULT 'Public',
    who_can_join ENUM('Anyone', 'Invite Only') DEFAULT 'Anyone',
    is_cancelled BOOLEAN DEFAULT false,
    author_id INT NOT NULL REFERENCES user(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS event_volunteer (
    event_id INT NOT NULL REFERENCES event(id),
    volunteer_id INT NOT NULL REFERENCES user(id),
    status ENUM('Invited', 'Maybe', 'Going', 'Cannot Go') DEFAULT 'Invited',
    PRIMARY KEY (event_id, volunteer_id)
);

CREATE TABLE IF NOT EXISTS event_post (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES user(id),
    event_id INT NOT NULL REFERENCES event(id),
    post_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES event(id)
);

CREATE TABLE IF NOT EXISTS event_post_pictures (
    event_post_id INT NOT NULL REFERENCES event_post(id),
    photo_url VARCHAR(256) NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (event_post_id, photo_url),
    CONSTRAINT unique_event_post_photo_url UNIQUE (event_post_id, photo_url)
);


CREATE TABLE  IF NOT EXISTS donation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('General', 'Event', 'Animal') NOT NULL, -- 'event' or 'org'
    animal_id INT,
    event_id INT,
    user_id INT NOT NULL REFERENCES user(id),
    donation_type ENUM('Money', 'In-Kind') NOT NULL, -- 'money' or 'in_kind'
    delivery_type ENUM('Pick-up', 'Deliver'), -- (if in_kind)
    pick_up_location VARCHAR(256), -- optional, depending on delivery_type
    amount INT, -- (if money)
    item_list TEXT, -- (if in-kind) [comma-seprated]
    remarks TEXT,
    is_confirmed BOOLEAN,
    thumbnail_url VARCHAR(256) DEFAULT NULL,
    FOREIGN KEY (animal_id) REFERENCES animal(id),
    FOREIGN KEY (event_id) REFERENCES event(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS donation_pictures (
    donation_id INT NOT NULL REFERENCES donation(id),
    photo_url VARCHAR(256) NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (donation_id, photo_url),
    CONSTRAINT unique_donation_photo_url UNIQUE (donation_id, photo_url)
);

CREATE TABLE IF NOT EXISTS donation_request (
    id INT AUTO_INCREMENT PRIMARY KEY,
    animal_id INT NOT NULL REFERENCES animal(id),
    description TEXT NOT NULL,
    amount INT, -- (if money)
    item_list TEXT, -- (if in-kind) [comma-separated]
    is_fulfilled BOOLEAN DEFAULT false,
    thumbnail_url VARCHAR(256) DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP  
);

CREATE TABLE IF NOT EXISTS donation_request_pictures (
    donation_request_id INT NOT NULL REFERENCES donation_request(id),
    photo_url VARCHAR(256) NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (donation_request_id, photo_url),
    CONSTRAINT unique_donation_request_photo_url UNIQUE (donation_request_id, photo_url)
);

CREATE TABLE IF NOT EXISTS donation_request_update (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES user(id),
    donation_request_id INT NOT NULL REFERENCES donation_request(id),
    update_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donation_request_id) REFERENCES donation_request(id)
);

CREATE TABLE IF NOT EXISTS donation_request_update_pictures (
    donation_request_update_id INT NOT NULL REFERENCES donation_request_update(id),
    photo_url VARCHAR(256) NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (donation_request_update_id, photo_url),
    CONSTRAINT unique_donation_request_update_photo_url UNIQUE (donation_request_update_id, photo_url)
);

CREATE TABLE IF NOT EXISTS donation_request_donation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES user(id),
    donation_request_id INT NOT NULL REFERENCES donation_request(id),
    donation_type ENUM('Money', 'In-Kind') NOT NULL, -- 'money' or 'in_kind'
    amount INT, -- (if money)
    item_list TEXT, -- (if in-kind) [comma-separated]
    is_confirmed BOOLEAN DEFAULT false,
    is_rejected BOOLEAN DEFAULT false,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donation_request_id) REFERENCES donation_request(id)
);

CREATE TABLE IF NOT EXISTS donation_request_donation_pictures (
    donation_request_donation_id INT NOT NULL REFERENCES donation_request_donation(id),
    photo_url VARCHAR(256) NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (donation_request_donation_id, photo_url),
    CONSTRAINT unique_donation_request_donation_photo_url UNIQUE (donation_request_donation_id, photo_url)
);

CREATE TABLE IF NOT EXISTS notification (
    id VARCHAR(32) PRIMARY KEY,
    type ENUM('ADOPTION_REQUEST', 'ADOPTION_STATUS_UPDATE', 'ADD_DONATION_MONEY', 'ADD_DONATION_IN_KIND', 'DONATION_STATUS_UPDATE', 'EVENT_INVITED'),
    animal_id INT,
    event_id INT,
    adoption_id INT,
    adoption_status_history_id INT,
    donation_id INT,
    user_who_fired_event_id INT NOT NULL,
    user_to_notify_id INT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    is_archived BOOLEAN DEFAULT false,
    FOREIGN KEY (animal_id) REFERENCES animal(id),
    FOREIGN KEY (adoption_id) REFERENCES adoption(id),
    FOREIGN KEY (adoption_status_history_id) REFERENCES adoption_status_history(id),
    FOREIGN KEY (donation_id) REFERENCES donation(id),
    FOREIGN KEY (event_id) REFERENCES event(id),
    FOREIGN KEY (user_who_fired_event_id) REFERENCES user(id),
    FOREIGN KEY (user_to_notify_id) REFERENCES user(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
