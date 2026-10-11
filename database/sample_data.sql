-- Sample data for Railway Reservation System
-- This file is optional and can be used manually for testing.

INSERT INTO users (name, email, password, role) VALUES
('Rahul Kumar', 'rahul@example.com', 'rahul123', 'user'),
('Amit Singh', 'amit@example.com', 'amit123', 'user');

INSERT INTO trains (train_number, train_name, source, destination, departure_time, arrival_time, duration, fare, total_seats, available_seats, class_type) VALUES
('12001', 'Bareilly Express', 'Bareilly', 'Delhi', '08:30', '11:15', '2h 45m', 420, 120, 76, 'Sleeper'),
('12487', 'Shatabdi Deluxe', 'Delhi', 'Agra', '09:00', '10:45', '1h 45m', 650, 90, 58, 'AC'),
('12911', 'Jaipur Queen', 'Agra', 'Jaipur', '14:20', '18:00', '3h 40m', 710, 110, 64, 'AC');
