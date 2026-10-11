DROP TABLE IF EXISTS cancellations;
DROP TABLE IF EXISTS waiting_list;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS trains;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user'
);

CREATE TABLE trains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_number TEXT NOT NULL,
    train_name TEXT NOT NULL,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    duration TEXT NOT NULL,
    fare REAL NOT NULL,
    total_seats INTEGER NOT NULL,
    available_seats INTEGER NOT NULL,
    class_type TEXT DEFAULT 'General'
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pnr TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    train_id INTEGER NOT NULL,
    passenger_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    journey_date TEXT NOT NULL,
    class TEXT NOT NULL,
    seat_number TEXT DEFAULT NULL,
    status TEXT DEFAULT 'CONFIRMED',
    booking_time TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (train_id) REFERENCES trains(id)
);

CREATE TABLE waiting_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    train_id INTEGER,
    passenger_name TEXT,
    pnr TEXT,
    position INTEGER,
    status TEXT DEFAULT 'WAITING',
    FOREIGN KEY (booking_id) REFERENCES bookings(id),
    FOREIGN KEY (train_id) REFERENCES trains(id)
);

CREATE TABLE cancellations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pnr TEXT NOT NULL,
    cancellation_time TEXT DEFAULT CURRENT_TIMESTAMP,
    refund_amount REAL DEFAULT 0,
    status TEXT DEFAULT 'CANCELLED'
);
