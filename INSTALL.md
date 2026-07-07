# Installation & Setup Guide

This project is fully containerized with Docker, meaning you do not need to install Python, Node.js, or MySQL on your local machine to run it.

## Prerequisites
* Git (to clone the repository)
* Docker Desktop (must be installed and running on your machine)

## How to Run
Clone the repository:
```bash
git clone https://github.com/sakalyeakshat/Smart-Car-recommendation-system.git
cd Smart-Car-recommendation-system
```

Start the containers
Run the following command in the root directory. This will download the necessary base images, install all dependencies, initialize the database, and start the network.
```bash
docker-compose up --build
```

## Access the Application
Once the terminal shows that both the backend and frontend servers are running, open your web browser:
* Frontend UI: http://localhost:3000
* Backend API: http://localhost:8000
* Swagger Docs: http://localhost:8000/docs
* ReDoc Docs: http://localhost:8000/redoc

## Stopping & Resetting
To gracefully stop the application: Press Ctrl + C in the terminal where Docker is running, or run:
```bash
docker-compose down
```

To perform a full hard reset: If you want to completely wipe the database and start from a completely clean slate (for example, to re-run the initialization script), use the -v flag to destroy the volumes before rebuilding:
```bash
docker-compose down -v
docker-compose up --build
```

## Environment Variables
Note: You do not need to manually create any .env files. All necessary development environment variables (like database credentials and ports) are safely handled and injected directly via the docker-compose.yml file.

## Running Without Docker (Optional)
If you prefer not to use Docker, you can run the services manually:

Backend:
1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. `pip install -r requirements.txt`
5. `uvicorn main:app --reload`

Frontend:
1. `cd frontend`
2. `npm install`
3. `npm start`
