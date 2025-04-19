# codex-sample-todolist

A simple Flask-based TODO list application.

## Requirements

- Python 3.7+
- Flask

## Setup

1. Clone the repository and enter the directory:

   git clone <repo-url>
   cd codex-sample-todolist

2. (Optional) Create and activate a virtual environment:

   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:

   pip install -r requirements.txt

4. Initialize the database:

   flask init-db

5. Run the application:

   flask run

The app will be available at http://127.0.0.1:5000.

## Docker Compose

You can also run the application using Docker Compose:

1. Build and start the service (database will be auto-initialized on first run):

   docker-compose up --build

2. The app will be available at http://localhost:5000.

3. (Optional) To reset the database:

   docker-compose run web flask init-db
