CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(256) UNIQUE NOT NULL,
    google_id VARCHAR(64),
    username VARCHAR(256) NOT NULL,
    first_name VARCHAR(256) NOT NULL,
    last_name VARCHAR(256) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    password VARCHAR(256) NOT NULL,
    photo_url VARCHAR(256),
    is_verified BOOLEAN DEFAULT 0,
    unread_notification_count INT DEFAULT 0,
    contact_number VARCHAR(12) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

--;;;;--

CREATE TABLE IF NOT EXISTS notification_settings (
    user_id INT PRIMARY KEY,
    
    adoption_request_web BOOLEAN DEFAULT 1,
    adoption_status_update_web BOOLEAN DEFAULT 1,
    add_donation_money_web BOOLEAN DEFAULT 1,
    add_donation_in_kind_web BOOLEAN DEFAULT 1,
    donation_status_update_web BOOLEAN DEFAULT 1,
    event_invited_web BOOLEAN DEFAULT 1,
    join_org_request_web BOOLEAN DEFAULT 1,
    confirm_join_org_request_web BOOLEAN DEFAULT 1,
    reject_join_org_request_web BOOLEAN DEFAULT 1,

    adoption_request_email BOOLEAN DEFAULT 1,
    adoption_status_update_email BOOLEAN DEFAULT 1,
    add_donation_money_email BOOLEAN DEFAULT 1,
    add_donation_in_kind_email BOOLEAN DEFAULT 1,
    donation_status_update_email BOOLEAN DEFAULT 1,
    event_invited_email BOOLEAN DEFAULT 1,
    join_org_request_email BOOLEAN DEFAULT 1,
    confirm_join_org_request_email BOOLEAN DEFAULT 1,
    reject_join_org_request_email BOOLEAN DEFAULT 1,
    
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

--;;;;--

CREATE TABLE IF NOT EXISTS role (
    name ENUM('Admin', 'Member', 'Non-Member') DEFAULT 'Member' PRIMARY KEY
);

--;;;;--

CREATE TABLE IF NOT EXISTS user_role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    role_name ENUM('Admin', 'Member', 'Non-Member'),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (role_name) REFERENCES role(name) ON DELETE CASCADE
);

--;;;;--

INSERT IGNORE INTO role (name) 
VALUES 
    ('Member'),
    ('Non-Member'),
    ('Admin');

--;;;;--

CREATE TRIGGER add_notification_settings AFTER INSERT ON user
FOR EACH ROW
BEGIN
    INSERT INTO notification_settings (user_id) VALUES (NEW.id);
END

--;;;;--

INSERT INTO user (email, username, first_name, last_name, gender, password, is_verified, contact_number, photo_url)
VALUES ('admin@isf.com', 'admin', 'Admin', 'User', 'Male', 'pbkdf2:sha256:600000$41AT9RlTuc6cKm5B$b6c91de61e1304dd5fd520c1465d097bf297441c00434ec650fed81c72013f8b', 1, '1234567890', 'isf/logo');

--;;;;--

INSERT INTO user_role (user_id, role_name) 
VALUES 
    ((SELECT id FROM user WHERE email = 'admin@isf.com'), 'Admin'),
    ((SELECT id FROM user WHERE email = 'admin@isf.com'), 'Member');

--;;;;--

CREATE TRIGGER assign_member_role AFTER INSERT ON user
FOR EACH ROW
BEGIN
    INSERT INTO user_role (user_id, role_name) VALUES (NEW.id, 'Non-Member');
END;

--;;;;--

CREATE TABLE IF NOT EXISTS animal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256) UNIQUE NOT NULL,
    type VARCHAR(16) NOT NULL,
    estimated_birth_month VARCHAR(16) NOT NULL,
    estimated_birth_year VARCHAR(16) NOT NULL,
    photo_url VARCHAR(256) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    is_adopted BOOLEAN NOT NULL,
    is_dead BOOLEAN NOT NULL,
    is_dewormed BOOLEAN NOT NULL,
    is_neutered BOOLEAN NOT NULL,
    in_shelter BOOLEAN NOT NULL,
    is_rescued BOOLEAN NOT NULL,
    for_adoption BOOLEAN DEFAULT 0,
    description TEXT,
    appearance TEXT,
    author_id INT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--;;;;--

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
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (animal_id) REFERENCES animal(id) ON DELETE CASCADE
);

--;;;;--

CREATE TABLE IF NOT EXISTS adoption_status_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    adoption_id INT NOT NULL,
    previous_status ENUM('Pending', 'Interview', 'Approved', 'Rejected', 'Turnovered'),
    new_status ENUM('Pending', 'Interview', 'Approved', 'Rejected', 'Turnovered') NOT NULL,
    remarks TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (adoption_id) REFERENCES adoption(id) ON DELETE CASCADE
);

--;;;;--

CREATE TRIGGER add_pending_adoption_history AFTER INSERT ON adoption
FOR EACH ROW
BEGIN
    INSERT INTO adoption_status_history (adoption_id, new_status) VALUES (NEW.id, 'Pending');
END;

--;;;;--

CREATE TABLE member_application (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    status ENUM('Confirmed', 'Rejected', 'Pending') DEFAULT 'Pending',
    join_reason TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

--;;;;--

CREATE TRIGGER confirm_member_application
AFTER UPDATE ON member_application
FOR EACH ROW
BEGIN
    IF NEW.status = 'Confirmed' THEN
        UPDATE user_role
        SET role_name = 'Member'
        WHERE user_id = NEW.user_id;
    END IF;
END;

--;;;;--

CREATE TABLE IF NOT EXISTS event (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256) UNIQUE NOT NULL,
    description TEXT,
    cover_photo_url VARCHAR(256),
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    location VARCHAR(256),
    who_can_see_it ENUM('Public', 'Verified Users', 'Members') DEFAULT 'Public',
    who_can_join ENUM('Anyone', 'Verified Users', 'Member-Only') DEFAULT 'Anyone',
    is_cancelled BOOLEAN DEFAULT false,
    author_id INT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--;;;;--

CREATE TABLE IF NOT EXISTS event_volunteer (
    event_id INT NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    volunteer_id INT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    status ENUM('Invited', 'Maybe', 'Going', 'Cannot Go') DEFAULT 'Invited',
    PRIMARY KEY (event_id, volunteer_id)
);

--;;;;--

CREATE TABLE IF NOT EXISTS event_post (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    event_id INT NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    post_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);

--;;;;--

CREATE TABLE IF NOT EXISTS event_post_pictures (
    event_post_id INT NOT NULL REFERENCES event_post(id) ON DELETE CASCADE,
    photo_url VARCHAR(256) NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (event_post_id, photo_url),
    CONSTRAINT unique_event_post_photo_url UNIQUE (event_post_id, photo_url)
);

--;;;;--

CREATE TABLE IF NOT EXISTS animal_help (
    id INT AUTO_INCREMENT PRIMARY KEY,
    animal_id INT NOT NULL REFERENCES animal(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    amount INT, 
    item_list TEXT,
    current_amount INT DEFAULT 0,
    is_fulfilled BOOLEAN DEFAULT false,
    thumbnail_url VARCHAR(256) DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP  
);

--;;;;--

CREATE TABLE IF NOT EXISTS animal_help_post (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    animal_help_id INT NOT NULL REFERENCES animal_help(id) ON DELETE CASCADE,
    post_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_help_id) REFERENCES animal_help(id) ON DELETE CASCADE
);

--;;;;--

CREATE TABLE IF NOT EXISTS animal_help_post_pictures (
    animal_help_post_id INT NOT NULL REFERENCES animal_help_post(id) ON DELETE CASCADE,
    photo_url VARCHAR(256) NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (animal_help_post_id, photo_url),
    CONSTRAINT unique_animal_help_post_photo_url UNIQUE (animal_help_post_id, photo_url)
);

--;;;;--

CREATE TABLE  IF NOT EXISTS donation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('General', 'Animal Help') NOT NULL, -- 'event' or 'org'
    animal_help_id INT,
    user_id INT NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    donation_type ENUM('Money', 'In-Kind') NOT NULL, -- 'money' or 'in_kind'
    amount INT, -- (if money)
    delivery_type ENUM('Pick-up', 'Deliver'), -- (if in_kind)
    pick_up_location VARCHAR(256), -- optional, depending on delivery_type
    item_list TEXT, -- (if in-kind) [comma-seprated]
    remarks TEXT,
    thumbnail_url TEXT,
    status ENUM('Pending', 'Confirmed', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (animal_help_id) REFERENCES animal_help(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

--;;;;--

CREATE TRIGGER update_current_amount_on_animal_help
AFTER UPDATE ON donation
FOR EACH ROW
BEGIN
    DECLARE donation_amount INT;

    IF NEW.donation_type = 'Money' AND NEW.type = 'Animal Help' AND NEW.status = 'Confirmed' THEN
        SET donation_amount = NEW.amount;
    ELSEIF NEW.donation_type = 'Money' AND NEW.type = 'Animal Help' AND NEW.status = 'Rejected' AND OLD.status = 'Confirmed' THEN
        SET donation_amount = -OLD.amount;
    ELSEIF NEW.donation_type = 'Money' AND NEW.type = 'Animal Help' AND NEW.status = 'Pending' AND OLD.status = 'Confirmed' THEN
        SET donation_amount = -OLD.amount;
    ELSE
        SET donation_amount = 0;
    END IF;

    UPDATE animal_help
    SET current_amount = current_amount + donation_amount
    WHERE id = NEW.animal_help_id;
END;

--;;;;--

CREATE TABLE IF NOT EXISTS donation_pictures (
    donation_id INT NOT NULL REFERENCES donation(id) ON DELETE CASCADE,
    photo_url VARCHAR(256) NOT NULL, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (donation_id, photo_url),
    CONSTRAINT unique_donation_photo_url UNIQUE (donation_id, photo_url)
);

--;;;;--

CREATE TABLE IF NOT EXISTS donation_status_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donation_id INT NOT NULL REFERENCES donation(id) ON DELETE CASCADE,
    previous_status ENUM('Pending', 'Confirmed', 'Rejected'),
    new_status ENUM('Pending', 'Confirmed', 'Rejected') NOT NULL,
    remarks TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

--;;;;--

CREATE TRIGGER add_pending_donation_history
AFTER INSERT ON donation
FOR EACH ROW
BEGIN
    INSERT INTO donation_status_history (donation_id, new_status)
    VALUES (NEW.id, 'Pending');
END;

--;;;;--

CREATE TRIGGER set_previous_status
BEFORE INSERT ON donation_status_history
FOR EACH ROW
SET NEW.previous_status = (
    SELECT new_status
    FROM donation_status_history
    WHERE donation_id = NEW.donation_id
    ORDER BY created_at DESC
    LIMIT 1
);

--;;;;--

CREATE TABLE IF NOT EXISTS notification (
    id VARCHAR(32) PRIMARY KEY,
    type ENUM(
        'ADOPTION_REQUEST', 
        'ADOPTION_STATUS_UPDATE', 
        'ADD_DONATION_MONEY', 
        'ADD_DONATION_IN_KIND', 
        'DONATION_STATUS_UPDATE', 
        'EVENT_INVITED', 
        'JOIN_ORG_REQUEST', 
        'CONFIRM_JOIN_ORG_REQUEST', 
        'REJECT_JOIN_ORG_REQUEST'
    ),
    animal_id INT,
    event_id INT,
    adoption_id INT,
    adoption_status_history_id INT,
    donation_id INT,
    donation_status_history_id INT,
    member_application_id INT,
    user_who_fired_event_id INT NOT NULL,
    user_to_notify_id INT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    is_archived BOOLEAN DEFAULT false,
    FOREIGN KEY (animal_id) REFERENCES animal(id) ON DELETE CASCADE,
    FOREIGN KEY (adoption_id) REFERENCES adoption(id) ON DELETE CASCADE,
    FOREIGN KEY (adoption_status_history_id) REFERENCES adoption_status_history(id) ON DELETE CASCADE,
    FOREIGN KEY (donation_id) REFERENCES donation(id) ON DELETE CASCADE,
    FOREIGN KEY (donation_status_history_id) REFERENCES donation_status_history(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE,
    FOREIGN KEY (member_application_id) REFERENCES member_application(id) ON DELETE CASCADE,
    FOREIGN KEY (user_who_fired_event_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (user_to_notify_id) REFERENCES user(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--;;;;--
