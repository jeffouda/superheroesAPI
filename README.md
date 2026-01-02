# Superheroes API

## Description
A Flask API for tracking heroes and their superpowers. This API allows users to view heroes, view powers, and assign powers to heroes with specific strength levels.

## Owner
Jeff H Ouda.

## Features

- **Heroes:** View a list of heroes and their details, including associated powers.
- **Powers:** View a list of powers and update their descriptions.
- **Hero Powers:** Assign powers to heroes (Many-to-Many relationship) with strength validation.
- **Validations:** Ensures data integrity (e.g., power descriptions must be at least 20 characters, strength must be 'Strong', 'Weak', or 'Average').
- **Email Functionality:** Send test emails via Flask-Mail.

## Setup Instructions

### Prerequisites
- Python 3.x
- pip

### Installation
1. Clone the Repository
```bash
git clone < https://github.com/jeffouda/superheroesAPI >
cd superheroes-api
```

2. Create a virtual environment 
```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up the database
```bash
flask db upgrade
python seed.py
```

5. Run the application
```bash
python app.py
```

The API will be available at `http://localhost:5000`.

## API Endpoints

- `GET /heroes` - List all heroes
- `GET /heroes/<id>` - Get a specific hero with powers
- `GET /powers` - List all powers
- `GET /powers/<id>` - Get a specific power
- `PATCH /powers/<id>` - Update a power's description
- `POST /hero_powers` - Create a hero-power relationship
- `GET /send_email` - Send a test email

## Support
For support or questions, contact jeff.ouda@student.moringaschool.com.

## License
This project is licensed under the MIT License.