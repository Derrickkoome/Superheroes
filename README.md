# Superheroes Flask API

A RESTful API built with Flask for managing superheroes, their powers, and the relationships between them.

## Features

- Manage heroes with their names and super names
- Track various superpowers with detailed descriptions
- Create associations between heroes and powers with strength ratings
- Full CRUD operations with proper validations
- Cascade delete functionality for maintaining data integrity

## Data Model

The API uses three main models:

- **Hero**: Represents a superhero with `name` and `super_name`
- **Power**: Represents a superpower with `name` and `description`
- **HeroPower**: Junction table linking heroes to powers with a `strength` attribute

### Relationships

- A Hero has many Powers through HeroPower
- A Power has many Heroes through HeroPower
- A HeroPower belongs to a Hero and a Power

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Superheroes
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. Seed the database with sample data:
```bash
python seed.py
```

6. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5555`

## API Endpoints

### GET /heroes

Returns a list of all heroes.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  }
]
```

### GET /heroes/:id

Returns details of a specific hero including their powers.

**Response (Success):**
```json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
    {
      "hero_id": 1,
      "id": 1,
      "power": {
        "description": "gives the wielder the ability to fly through the skies at supersonic speed",
        "id": 2,
        "name": "flight"
      },
      "power_id": 2,
      "strength": "Strong"
    }
  ]
}
```

**Response (Not Found):**
```json
{
  "error": "Hero not found"
}
```

### GET /powers

Returns a list of all powers.

**Response:**
```json
[
  {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  }
]
```

### GET /powers/:id

Returns details of a specific power.

**Response (Success):**
```json
{
  "id": 1,
  "name": "super strength",
  "description": "gives the wielder super-human strengths"
}
```

**Response (Not Found):**
```json
{
  "error": "Power not found"
}
```

### PATCH /powers/:id

Updates a power's description.

**Request Body:**
```json
{
  "description": "Valid Updated Description"
}
```

**Response (Success):**
```json
{
  "id": 1,
  "name": "super strength",
  "description": "Valid Updated Description"
}
```

**Response (Validation Error):**
```json
{
  "errors": ["description must be at least 20 characters"]
}
```

### POST /hero_powers

Creates a new association between a hero and a power.

**Request Body:**
```json
{
  "strength": "Average",
  "power_id": 1,
  "hero_id": 3
}
```

**Response (Success):**
```json
{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Average",
  "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
  },
  "power": {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  }
}
```

**Response (Validation Error):**
```json
{
  "errors": ["strength must be one of: Strong, Weak, Average"]
}
```

## Validations

### HeroPower Model
- `strength` must be one of: 'Strong', 'Weak', or 'Average'

### Power Model
- `description` must be present and at least 20 characters long

## Testing

A Postman collection is available for testing all endpoints. Import the collection into Postman and test against `http://localhost:5555`.

## Technologies Used

- Flask 2.2.5
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 4.1.0
- SQLite (development database)

## Project Structure

```
Superheroes/
├── app.py              # Main application file with routes
├── models.py           # Database models
├── db.py               # Database initialization
├── seed.py             # Database seeding script
├── requirements.txt    # Python dependencies
├── Pipfile             # Pipenv dependencies
├── README.md           # This file
└── development.db      # SQLite database (generated)
```

## License

This project is open source and available for educational purposes.
