# 🏠 C#28 🎓 – HBnB Team Project – Part 2

## 🏠 Overview

HBnB is a backend web application inspired by AirBnB, developed as part of the Holberton School curriculum.

This second part focuses on building:

- The Business Logic Layer

- The RESTful API (Presentation Layer)

- A clean and modular backend architecture

The project is built using Python, Flask, and Flask-RESTx, following layered architecture principles and applying the Facade Design Pattern.

## 🎯 Project Goals

By the end of Part 2, the application supports:

- Modular Flask application structure

- Object modeling with relationships

- RESTful CRUD endpoints

- In-memory persistence layer

- Separation of concerns (API / Business / Persistence)

- Data validation and serialization

- Unit and integration testing

## 🧱 Architecture Overview

The application follows a layered architecture to ensure scalability and maintainability.

### 1. API Layer (Presentation)

- Built with Flask and Flask-RESTx

- Defines REST endpoints

- Handles request parsing and response formatting

- Automatically generates Swagger documentation

Location:
```code
app/api/v1/
```
### 2. Business Logic Layer

Contains all domain models and application logic.

Implemented Models:

**BaseModel**

- id (UUID)

- created_at

- updated_at

**User**

- first_name

- last_name

- email

- password (not exposed in API)

**Place**

- title

- description

- price

- latitude / longitude

- owner (User relationship)

- amenities (Many-to-Many)

**Amenity**

- name

**Review**

- text

- rating

- linked to User and Place

Location:
```code
app/models/
```

### 3. Persistence Layer

- In-memory repository implementation

- Abstracted storage layer

- Easily replaceable with database (PostgreSQL, MySQL, etc.)

Location:
```code
app/persistence/repository.py
```

### 4. Facade Layer

The Facade pattern is used to:

- Centralize business operations

- Decouple API from model logic

- Provide a clean service interface


Location:
```code
app/services/facade.py
```

## 🗂️ Project Structure
```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── basemodel.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   └── facade.py
│   ├── persistence/
│   │   └── repository.py
├── tests/
├── run.py
├── config.py
├── requirements.txt
```



## 🚀 API Endpoints
All routes are prefixed with:
```bash
/api/v1/
```

## 👤 Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | users | Create a user |
| GET | users | List users |
| GET | users/<id> | Get user by ID |
| PUT | users/<id> | Update user |


## 🏷️ Amenities

| Method | Endpoint | Description |
|--------|----------|------------ |
| POST | amenities | Create |
| GET	| amenities | List all |
| GET	| amenities/<id> | Retrieve one |
| PUT	| amenities/<id> | Update |

## 🏠 Places

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | places | Create place |
| GET | places | List all places |
| GET | places/<id> | Retrieve place (with owner & amenities) |
| PUT | places/<id> | Update |

## 📝 Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | reviews | Create |
| GET | reviews | List |
| GET | reviews/<id> | Retrieve |
| PUT | reviews/<id> | Update |
| DELETE | reviews/<id> | Delete |

✅ DELETE available only for Reviews.

## 🧪 Testing

### ✅ Run Unit Tests

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 -m unittest discover tests
```
##  ▶️ Running the Application
###  1️⃣ Install dependencies
```bash
pip3 install -r requirements.txt
```
##  2️⃣ Start the server

```bash
python3 run.py
```

Server will run on:
```code
http://localhost:5000
```

Swagger documentation:
```code
http://localhost:5000/api/v1/
```

##  🧪 Example cURL Request

Create a user:
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name":"Alice","last_name":"Doe","email":"alice@example.com"}'
```
##  🛠️ Technologies Used

- Python 3

- Flask

- Flask-RESTx

- unittest

- UUID

- RESTful API principles

## ✍️ Author

👥 [Jarod Lange](https://github.com/JarodLgeOff)

👥 [Cyril Iglesias](https://github.com/Iglcyril)