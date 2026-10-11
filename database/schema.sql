CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS trains (
    id INT PRIMARY KEY AUTO_INCREMENT,
    train_number VARCHAR(20) NOT NULL,
    train_name VARCHAR(100) NOT NULL,
    source VARCHAR(50) NOT NULL,
    destination VARCHAR(50) NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    duration VARCHAR(20) NOT NULL,
    fare DECIMAL(10,2) NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL,
    class_type VARCHAR(50) DEFAULT 'General'
);

CREATE TABLE IF NOT EXISTS bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pnr VARCHAR(20) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    train_id INT NOT NULL,
    passenger_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    journey_date DATE NOT NULL,
    class VARCHAR(50) NOT NULL,
    seat_number VARCHAR(50) DEFAULT NULL,
    status VARCHAR(20) DEFAULT 'CONFIRMED',
    booking_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (train_id) REFERENCES trains(id)
);

CREATE TABLE IF NOT EXISTS waiting_list (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT,
    train_id INT,
    passenger_name VARCHAR(100),
    pnr VARCHAR(20),
    position INT,
    status VARCHAR(20) DEFAULT 'WAITING',
    FOREIGN KEY (booking_id) REFERENCES bookings(id),
    FOREIGN KEY (train_id) REFERENCES trains(id)
);

CREATE TABLE IF NOT EXISTS cancellations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pnr VARCHAR(20) NOT NULL,
    cancellation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    refund_amount DECIMAL(10,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'CANCELLED'
);

INSERT INTO users (name, email, password, role) VALUES
('Admin User', 'admin@railway.com', '$2b$12$5pg8LsbJ1hGzjA0fAgc3mOQ4m.Nt3UMCBkR5s7S8mP7S7zZH3pXb2', 'admin'),
('Rahul Kumar', 'rahul@example.com', '$2b$12$W3O3I5S3Zy13ZQE0yw5kt.0kLad8vPztG3dVfXvQwZxW4P4mBR9aG', 'user'),
('Amit Singh', 'amit@example.com', '$2b$12$5sU.9n0cB4nWQmK7.0Pdh.W7vY4Vv6lBLpV8eNl6lAq6oN4JHnIea', 'user');

INSERT INTO trains (train_number, train_name, source, destination, departure_time, arrival_time, duration, fare, total_seats, available_seats, class_type) VALUES
('12001', 'Bareilly Express', 'Bareilly', 'Delhi', '08:30:00', '11:15:00', '2h 45m', 420.00, 120, 76, 'Sleeper'),
('12487', 'Shatabdi Deluxe', 'Delhi', 'Agra', '09:00:00', '10:45:00', '1h 45m', 650.00, 90, 58, 'AC'),
('12911', 'Jaipur Queen', 'Agra', 'Jaipur', '14:20:00', '18:00:00', '3h 40m', 710.00, 110, 64, 'AC'),
('14221', 'Lucknow Mail', 'Lucknow', 'Kanpur', '07:15:00', '09:10:00', '1h 55m', 350.00, 100, 67, 'Sleeper'),
('12345', 'Northern Link', 'Bareilly', 'Lucknow', '18:50:00', '21:40:00', '2h 50m', 480.00, 130, 82, 'Sleeper'),
('15012', 'Rajasthan Wing', 'Jaipur', 'Jodhpur', '06:10:00', '10:20:00', '4h 10m', 780.00, 140, 92, 'AC');
