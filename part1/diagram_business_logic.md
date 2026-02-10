```mermaid
classDiagram
    direction TB
    
    %% Classe abstraite BaseModel
    class BaseModel {
        <<abstract>>
        -string id
        -datetime created_at
        -datetime updated_at
        
    
        +to_dict() dict
    }
    
    %% Classe User
    class User {
        -string first_name
        -string last_name
        -string email
        -string password
        -boolean is_admin
        
        +create(data) User
        +read(id) User
        +update(id, data) User
       
    }
    
    %% Classe Place
    class Place {
        -string title
        -string description
        -float price
        -float latitude
        -float longitude
        -string owner_id
        -list~string~ amenity_ids
        
        +create(data) Place
        +update(id, data) Place
        +add_amenity(amenity_id) void
        +remove_amenity(amenity_id) void
        +validate_price() boolean
        +validate_coordinates() boolean
    }
    
    %% Classe Review
    class Review {
        -string place_id
        -string user_id
        -int rating
        -string comment
        
        +create(data) Review
        +update(id, data) Review
        +validate_rating(rating) boolean
    }
    
    %% Classe Amenity
    class Amenity {
        -string name
        -string description
        
        +create(data) Amenity
        +update(id, data) Amenity
    }
    
    %% Héritage (toutes les classes héritent de BaseModel)
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity
    
    %% Relations entre entités
    User --> Place : owns
    User --> Review : writes
    Place --> Review : has
    Place o-- Amenity : includes
	```