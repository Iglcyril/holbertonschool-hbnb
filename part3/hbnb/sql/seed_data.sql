-- HBnB Seed Data Script
-- This script inserts initial data: admin user and default amenities

-- Insert administrator user
-- Password: admin1234 (hashed with bcrypt)
-- ID is fixed for consistency: 36c9050e-ddd3-4c3b-9731-9f487208bbc1
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqPjKKYqKm',  -- Hash of 'admin1234'
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert default amenities
-- WiFi
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    UUID(),
    'WiFi',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Swimming Pool
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    UUID(),
    'Swimming Pool',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
