-- HBnB Seed Data Script
-- This script inserts initial data: admin user and default amenities
-- Compatible with SQLite (no UUID() function, no ON UPDATE syntax)
 
-- Insert administrator user
-- Password: admin1234 (hashed with bcrypt)
-- ID is fixed for consistency: 240cb0dd-ce42-4a4d-9264-4810c8ddcd2e
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '240cb0dd-ce42-4a4d-9264-4810c8ddcd2e',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqPjKKYqKm',
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
 
-- Insert default amenities (UUIDs fixes, compatibles SQLite)
-- WiFi
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'a1b2c3d4-e5f6-7890-abcd-ef1234567801',
    'WiFi',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
 
-- Swimming Pool
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'a1b2c3d4-e5f6-7890-abcd-ef1234567802',
    'Swimming Pool',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
 
-- Air Conditioning
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'a1b2c3d4-e5f6-7890-abcd-ef1234567803',
    'Air Conditioning',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
 
-- Kitchen
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'a1b2c3d4-e5f6-7890-abcd-ef1234567804',
    'Kitchen',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
 
-- Parking
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'a1b2c3d4-e5f6-7890-abcd-ef1234567805',
    'Parking',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
