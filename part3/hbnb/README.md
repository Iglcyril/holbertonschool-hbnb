# 🏠 C#28 🎓 – HBnB Team Project – Parts 2 & 3

## 🏠 Overview

HBnB is a backend web application inspired by AirBnB, developed as part of the Holberton School curriculum.

**Part 2** focused on building the Business Logic Layer and RESTful API with in-memory persistence.

**Part 3** extends the application with:
- JWT-based authentication and authorization
- SQLAlchemy ORM with SQLite/MySQL database
- Password hashing with bcrypt
- Role-based access control (admin/user)
- Persistent data storage
- Database relationships (One-to-Many, Many-to-Many)

The project is built using Python, Flask, Flask-RESTx, SQLAlchemy, and follows layered architecture principles with the Facade Design Pattern.

## 🎯 Project Goals

By the end of Part 3, the application supports:

- ✅ Secure user authentication with JWT tokens
- ✅ Password hashing with bcrypt
- ✅ Role-based authorization (admin vs regular users)
- ✅ SQLite database for development
- ✅ MySQL-ready for production
- ✅ Database relationships and constraints
- ✅ RESTful CRUD endpoints with authentication
- ✅ Data validation and serialization
- ✅ Automated database initialization scripts

## 🧱 Architecture Overview

The application follows a layered architecture to ensure scalability and maintainability.

### 1. API Layer (Presentation)

- Built with Flask and Flask-RESTx
- Defines REST endpoints with JWT protection
- Handles request parsing and response formatting
- Automatically generates Swagger documentation with JWT authorization

Location:
```
app/api/v1/
```

### 2. Business Logic Layer

Contains all domain models and application logic.

**Implemented Models:**

**BaseModel** (SQLAlchemy Abstract Base)
- id (UUID, Primary Key)
- created_at (DateTime)
- updated_at (DateTime)

**User**
- first_name (VARCHAR 50)
- last_name (VARCHAR 50)
- email (VARCHAR 120, UNIQUE)
- password (VARCHAR 255, hashed with bcrypt)
- is_admin (BOOLEAN, default False)
- **Relationships:** places (One-to-Many), reviews (One-to-Many)

**Place**
- title (VARCHAR 100)
- description (VARCHAR 500)
- price (FLOAT)
- latitude (FLOAT)
- longitude (FLOAT)
- owner_id (Foreign Key → users.id)
- **Relationships:** owner (Many-to-One), reviews (One-to-Many), amenities (Many-to-Many)

**Amenity**
- name (VARCHAR 50, UNIQUE)
- **Relationships:** places (Many-to-Many)

**Review**
- text (VARCHAR 1000)
- rating (INTEGER, 1-5)
- place_id (Foreign Key → places.id)
- user_id (Foreign Key → users.id)
- **Constraints:** UNIQUE(user_id, place_id) - one review per user per place
- **Relationships:** place (Many-to-One), user (Many-to-One)

**Place_Amenity** (Association Table)
- place_id (Foreign Key → places.id)
- amenity_id (Foreign Key → amenities.id)
- **Composite Primary Key:** (place_id, amenity_id)

Location:
```
app/models/
```

### 3. Persistence Layer

**Part 2:** In-memory repository implementation

**Part 3:** SQLAlchemy ORM with database persistence
- SQLite for development
- MySQL for production
- Repository pattern maintained for consistency

Location:
```
app/persistence/repository.py
app/persistence/SQLAlchemyRepository.py
```

### 4. Facade Layer

The Facade pattern is used to:
- Centralize business operations
- Decouple API from model logic
- Provide a clean service interface
- Handle database transactions

Location:
```
app/services/facade.py
```

## 🗂️ Project Structure
```
hbnb/
├── app/
│   ├── __init__.py                    
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py                
│   │       ├── users.py               
│   │       ├── places.py              
│   │       ├── reviews.py             
│   │       └── amenities.py           
│   ├── models/
│   │   ├── BaseModel.py               
│   │   ├── user.py                    
│   │   ├── place.py                  
│   │   ├── review.py                  
│   │   └── amenity.py                 
│   ├── services/
│   │   └── facade.py                  
│   ├── persistence/
│   │   ├── repository.py              
│   │   └── SQLAlchemyRepository.py    
├── sql/
│   ├── init_db.sql                    
│   ├── seed_data.sql                  
│   └── database_diagram.md            
├── instance/
│   └── development.db                 
├── tests/
├── run.py                             
├── config.py                          
└── requirements.txt                   
```

## 🔐 Authentication & Authorization

### JWT Authentication (Part 3)

**Login:**
```bash
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Using the token:**
Add to request headers:
```
Authorization: Bearer <your_token_here>
```

### Protected Endpoints

**Authenticated Users can:**
- Create, update, delete their own places
- Create, update, delete their own reviews
- Update their own user profile (except email/password)

**Admin Users can:**
- Create any user
- Update any user (including email/password)
- Create, update amenities
- Bypass ownership restrictions on places/reviews

### Business Rules

- Users cannot review their own places
- Users can only submit one review per place
- Ratings must be between 1 and 5
- Passwords are hashed with bcrypt (never stored in plain text)
- Email addresses must be unique

## 🚀 API Endpoints

All routes are prefixed with:
```
/api/v1/
```

### 🔓 Public Endpoints (No authentication required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Login and get JWT token |
| GET | `/places/` | List all places |
| GET | `/places/<id>` | Get place details |

### 🔐 Authenticated Endpoints (JWT required)

#### 👤 Users

| Method | Endpoint | Description | Auth Level |
|--------|----------|-------------|------------|
| POST | `/users/` | Create user | Admin only |
| GET | `/users/` | List users | Public |
| GET | `/users/<id>` | Get user by ID | Public |
| PUT | `/users/<id>` | Update user | Owner or Admin |

#### 🏠 Places

| Method | Endpoint | Description | Auth Level |
|--------|----------|-------------|------------|
| POST | `/places/` | Create place | Authenticated |
| GET | `/places/` | List places | Public |
| GET | `/places/<id>` | Get place | Public |
| PUT | `/places/<id>` | Update place | Owner or Admin |

#### 📝 Reviews

| Method | Endpoint | Description | Auth Level |
|--------|----------|-------------|------------|
| POST | `/reviews/` | Create review | Authenticated |
| GET | `/reviews/` | List reviews | Public |
| GET | `/reviews/<id>` | Get review | Public |
| PUT | `/reviews/<id>` | Update review | Owner or Admin |
| DELETE | `/reviews/<id>` | Delete review | Owner or Admin |

#### 🏷️ Amenities

| Method | Endpoint | Description | Auth Level |
|--------|----------|-------------|------------|
| POST | `/amenities/` | Create amenity | Admin only |
| GET | `/amenities/` | List amenities | Public |
| GET | `/amenities/<id>` | Get amenity | Public |
| PUT | `/amenities/<id>` | Update amenity | Admin only |

## 📊 Database Schema

### Entity Relationship Diagram
```mermaid
erDiagram
    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : has
    PLACES }o--o{ AMENITIES : includes
    
    USERS {
        string id PK
        string first_name
        string last_name
        string email UK
        string password
        boolean is_admin
        datetime created_at
        datetime updated_at
    }
    
    PLACES {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
        datetime created_at
        datetime updated_at
    }
    
    REVIEWS {
        string id PK
        string text
        integer rating
        string place_id FK
        string user_id FK
        datetime created_at
        datetime updated_at
    }
    
    AMENITIES {
        string id PK
        string name UK
        datetime created_at
        datetime updated_at
    }
    
    PLACE_AMENITY {
        string place_id PK,FK
        string amenity_id PK,FK
    }
```

### Database Initialization

**Create tables:**
```bash
mysql -u root -p < sql/init_db.sql
```

**Insert initial data (admin + amenities):**
```bash
mysql -u root -p < sql/seed_data.sql
```

**Default admin credentials:**
- Email: `admin@hbnb.io`
- Password: `admin1234`
- ID: `36c9050e-ddd3-4c3b-9731-9f487208bbc1`

## ▶️ Running the Application

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Configure database (optional)

Edit `config.py` to switch between SQLite and MySQL:

**SQLite (default for development):**
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
```

**MySQL (for production):**
```python
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/hbnb_db'
```

### 3️⃣ Initialize the database
```bash
python -m flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

Or use SQL scripts:
```bash
mysql -u root -p < sql/init_db.sql
mysql -u root -p < sql/seed_data.sql
```

### 4️⃣ Start the server
```bash
python run.py
```

Server will run on:
```
http://localhost:5000
```

Swagger documentation with JWT authorization:
```
http://localhost:5000/
```

## 🧪 Testing

### API Testing with Swagger UI

1. Navigate to `http://localhost:5000/`
2. Click **Authorize** 🔒 button
3. Login via `/auth/login` to get JWT token
4. Enter token as: `Bearer <your_token>`
5. Test protected endpoints

### Example cURL Requests

**Create a user:**
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Alice",
  "last_name": "Doe",
  "email": "alice@example.com",
  "password": "securepass123"
}'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
-H "Content-Type: application/json" \
-d '{
  "email": "alice@example.com",
  "password": "securepass123"
}'
```

**Create a place (with JWT):**
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_token>" \
-d '{
  "title": "Beach House",
  "description": "Beautiful sea view",
  "price": 150.0,
  "latitude": 43.7102,
  "longitude": 7.2620,
  "owner_id": "<user_id>",
  "amenities": ["<amenity_id1>", "<amenity_id2>"]
}'
```

### Unit Tests
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python -m unittest discover tests
```

## 🛠️ Technologies Used

### Backend Framework
- Python 3
- Flask
- Flask-RESTx
- Flask-SQLAlchemy

### Security
- Flask-Bcrypt (password hashing)
- Flask-JWT-Extended (authentication)

### Database
- SQLAlchemy ORM
- SQLite (development)
- MySQL (production-ready)

### Testing & Documentation
- unittest
- Swagger UI (auto-generated)
- Mermaid.js (ER diagrams)

## 📚 Key Features Added in Part 3

✅ **JWT Authentication** - Secure token-based auth  
✅ **Password Hashing** - Bcrypt for secure storage  
✅ **Role-Based Access Control** - Admin vs User permissions  
✅ **Database Persistence** - SQLite/MySQL with SQLAlchemy  
✅ **Relationships** - Foreign keys and Many-to-Many  
✅ **Constraints** - UNIQUE, CHECK, CASCADE  
✅ **SQL Scripts** - Database initialization and seeding  
✅ **ER Diagram** - Visual database schema  

## ✍️ Authors

👥 [Jarod Lange](https://github.com/JarodLgeOff)  
👥 [Cyril Iglesias](https://github.com/Iglcyril)

---

**🎓 Holberton School - C#28 - HBnB Evolution Project**