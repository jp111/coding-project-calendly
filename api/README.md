# Calendly API

This project is a simple implementation of a scheduling API, inspired by Calendly, that allows users to manage their availability and find overlapping available slots between two users. The project uses a MongoDB database to store availability data.

## Features

- Initialize a new user with all time slots unavailable.
- Set availability for specific time slots.
- Update availability for multiple time slots.
- Check if a user is available at a specific time.
- Find all available slots within a given time range.
- Find overlapping available slots between two users.

## Assumptions

1. **Time Slots**: Each day is divided into 48 half-hour slots.
2. **Availability**: By default, all slots are unavailable for a new user.
3. **Time Format**: Time should be provided in HH:MM format, with minutes being either `00` or `30`.

## System Specifications

- Python 3.8+
- MongoDB 4.0+

## Modules Required

- `pymongo`
- `flask`
- `unittest`

You can install the required modules using pip:
```bash
pip install pymongo flask


DIRECTORY STRUCTURE

calendly_api/
├── __init__.py
├── api
│   ├── README.md
│   ├── __init__.py
│   └── endpoints.py
├── calendly_api
│   ├── __init__.py
│   ├── config
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── database
│   │   ├── __init__.py
│   │   └── mongo_client.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── availability.py
│   ├── services
│   │   ├── __init__.py
│   │   └── availability_service.py
│   └── tests
│       ├── __init__.py
│       └── test_availability_service.py
└── requirements.txt



CONFIGURATION
MONGO_URI = "mongodb://localhost:27017/"

Running the Application
1. Start MongoDB: Ensure MongoDB is running on your local machine on port 27017.

2. Run the Flask Application:
    ~/export FLASK_APP=calendly_api/app.py
    ~/flask run

3. Running Tests
    ~/PYTHONPATH=. python -m unittest discover -s calendly_api/tests

API Endpoints
Initialize User
Endpoint: POST /initialize_user/<user_id>

Description: Initialize a new user with all time slots unavailable.

Set Availability
Endpoint: POST /set_availability

Description: Set availability for specific time slots.

Request Body:

{
  "user_id": "user1",
  "start_time": "09:00",
  "end_time": "10:00",
  "available": true
}

Update Availability
Endpoint: POST /update_availability

Description: Update availability for multiple time slots.

Request Body:

{
  "user_id": "user1",
  "updates": [
    {
      "start_time": "09:00",
      "end_time": "10:00",
      "available": true
    },
    {
      "start_time": "11:00",
      "end_time": "12:00",
      "available": false
    }
  ]
}

Check Availability
Endpoint: GET /is_available/<user_id>/<time>

Description: Check if a user is available at a specific time.

Find Availability
Endpoint: GET /find_availability/<user_id>/<start_time>/<end_time>

Description: Find all available slots within a given time range.

Find Overlap
Endpoint: GET /find_overlap/<user1_id>/<user2_id>

Description: Find overlapping available slots between two users.

Running Tests
To run the tests, use the following command:

~/python3 -m unittest discover -s calendly_api/tests


Edge Cases Handled
* User Not Initialized: If a user is not initialized, the system will automatically initialize the user with all time slots unavailable.
* Invalid Time Format: The system raises an error if the time format is invalid.
* Time Outside of Range: The system raises an error if the time is outside the range of 00:00 to 23:30.



