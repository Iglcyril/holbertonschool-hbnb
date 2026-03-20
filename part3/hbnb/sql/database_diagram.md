erDiagram
    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : has
    PLACES }o--o{ AMENITIES : includes
    
    USERS {
        string id PK "UUID, Primary Key"
        string first_name "VARCHAR(50), NOT NULL"
        string last_name "VARCHAR(50), NOT NULL"
        string email "VARCHAR(120), UNIQUE, NOT NULL"
        string password "VARCHAR(255), NOT NULL"
        boolean is_admin "DEFAULT FALSE"
        datetime created_at "Timestamp"
        datetime updated_at "Timestamp"
    }
    
    PLACES {
        string id PK "UUID, Primary Key"
        string title "VARCHAR(100), NOT NULL"
        string description "VARCHAR(500)"
        float price "NOT NULL"
        float latitude "NOT NULL"
        float longitude "NOT NULL"
        string owner_id FK "Foreign Key -> USERS.id"
        datetime created_at "Timestamp"
        datetime updated_at "Timestamp"
    }
    
    REVIEWS {
        string id PK "UUID, Primary Key"
        string text "VARCHAR(1000), NOT NULL"
        integer rating "1-5, NOT NULL"
        string place_id FK "Foreign Key -> PLACES.id"
        string user_id FK "Foreign Key -> USERS.id"
        datetime created_at "Timestamp"
        datetime updated_at "Timestamp"
    }
    
    AMENITIES {
        string id PK "UUID, Primary Key"
        string name "VARCHAR(50), UNIQUE, NOT NULL"
        datetime created_at "Timestamp"
        datetime updated_at "Timestamp"
    }
    
    PLACE_AMENITY {
        string place_id PK,FK "Foreign Key -> PLACES.id"
        string amenity_id PK,FK "Foreign Key -> AMENITIES.id"
    }
