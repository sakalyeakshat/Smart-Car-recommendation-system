# 🚗 DriveMatch AI

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)
![React](https://img.shields.io/badge/React-Frontend-61DAFB.svg)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)
---

# 📖 Project Overview

DriveMatch AI is a **Smart Car Recommendation System** that generates personalized vehicle recommendations based on a user's profile and preferences.

Users provide information such as:

* Budget (in Lakhs)
* Fuel Type Preference (Petrol, Diesel, CNG, Electric)
* Transmission Preference (Manual, Automatic)
* Seating Capacity
* Minimum Safety Rating (NCAP Stars)
* Body Type (Hatchback, Sedan, SUV, MUV)
* Minimum Mileage (kmpl)

Based on these inputs, the application recommends an optimized vehicle selection using a weighted multi-criteria recommendation engine backed by a MySQL database.

---

# ✨ Features

* Personalized car recommendations with explanation badges
* Brand diversity filtering to ensure a variety of choices
* "Explore More" details listing key strengths and trade-offs
* FastAPI backend
* React frontend
* MySQL database
* Dockerized architecture
* Docker Compose support
* Responsive user interface
* Input validation using Pydantic

---

# 🛠 Technology Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn
* PyMySQL
* Pandas

## Frontend

* React
* Axios
* CSS

## Database

* MySQL

## DevOps

* Docker
* Docker Compose

---

# 🏗 Project Architecture

```text
                    User
                      │
                      ▼
               React Frontend
                      │
              FAST API Requests
                      │
                      ▼
              FastAPI Backend
                      │
            Recommendation Engine
                      │
                      ▼
               MySQL Database
```

---

# 📂 Project Structure

```text
Smart-Car-recommendation-system/
│
├── backend/
│   ├── app/
│   │   ├── recommendation/
│   │   │   └── recommend.py               # Weighted scoring and brand diversity logic
│   │   ├── routers/
│   │   │   ├── recommendation.py          # /recommend endpoint
│   │   │   └── explore.py                 # /explore endpoint
│   │   ├── schemas/
│   │   │   ├── request.py                 # Pydantic input models
│   │   │   ├── response.py                # Pydantic response models
│   │   │   └── explore.py                 # Pydantic explore models
│   │   ├── services/
│   │   │   └── recommendation_service.py  # Seeding & DB queries
│   │   ├── config.py                      # Weight coefficients and configurations
│   │   └── main.py                        # FastAPI entrypoint & CORS setup
│   ├── database/
│   │   └── database.py                    # Database connection setup
│   ├── datasets/
│   │   ├── raw/
│   │   │   └── cars_in.csv                # Source Indian Cars dataset
│   │   └── explore_and_clean.ipynb        # Jupyter Notebook for cleaning steps
│   ├── dockerfile                         # Backend container config
│   ├── requirements.txt                   # Backend dependencies
│   └── start.sh                           # Startup shell script waiting for MySQL
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CarCard.jsx                # Render single recommended car
│   │   │   ├── ExploreModal.jsx           # Strengths/trade-offs detail modal
│   │   │   ├── Hero.jsx                   # Hero landing element
│   │   │   ├── RecommendationPage.jsx     # Input questionnaire form
│   │   │   ├── ResultsPage.jsx            # Display recommended cars grid
│   │   │   └── Services.jsx               # Feature highlights section
│   │   ├── styles/                        # Custom stylesheet components
│   │   ├── App.css                        # Global styling definitions
│   │   ├── App.js                         # React main router & view controller
│   │   ├── index.css
│   │   └── index.js
│   ├── dockerfile                         # Frontend container config
│   └── package.json                       # Node dependencies & run scripts
│
├── mysql/
│   └── init.sql                           # Database initialization schema
│
├── docker-compose.yml                     # Orchestration configuration
│
└── README.md                              # Project Documentation
```

---

# ⚙️ Installation

## Prerequisites

Install the following software before running the project:

* Docker

---

# Clone the Repository

```bash
git clone https://github.com/akshats24/Smart-Car-recommendation-system.git

cd Smart-Car-recommendation-system
```

---

# Run Using Docker (Recommended)

Build and start all containers:

```bash
docker compose up
```

Stop containers:

```bash
docker compose down
```

Remove volumes:

```bash
docker compose down -v
```

---

# Application URLs

Frontend

http://localhost:3000

Backend

http://localhost:8000

Swagger Documentation

http://localhost:8000/docs

ReDoc Documentation

http://localhost:8000/redoc


---

# Running Without Docker

## Backend

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn app.main:app --reload
```

---

## Frontend

Install dependencies

```bash
npm install
```

Run development server

```bash
npm start
```

---

# Database Setup

The application uses MySQL.

If using Docker, the database is automatically created during startup.

The initialization script creates:

* Database
* Required tables
* Seeds initial car data from `cars_in.csv`

---

# How the Recommendation Engine Works

1. User enters car preferences.
2. Frontend validates the form.
3. Data is sent to the FastAPI backend.
4. Backend validates the request using Pydantic.
5. Recommendation engine queries the MySQL database.
6. Cars are filtered and scored based on budget and seating constraints.
7. Matching vehicles are evaluated using a weighted multi-criteria scoring algorithm.
8. A brand diversity pass ensures recommendations span different manufacturers.
9. Personalized car recommendation list is generated.
10. Results are returned as JSON.
11. Frontend displays the recommended cars.

---

# User Inputs

The recommendation engine considers factors such as:

* Budget (in Lakhs)
* Fuel Type
* Transmission Type
* Seating Capacity
* Safety Rating
* Body Type
* Minimum Mileage

These inputs help generate recommendations that are more relevant than generic car listings.

---

# Validation

The backend validates all incoming requests using Pydantic.

Examples include:

* Missing fields
* Invalid values
* Incorrect data types
* Empty requests

Appropriate HTTP status codes are returned when validation fails.

---

# Docker Containers

The application consists of three independent containers:

## Frontend

* React

## Backend

* FastAPI
* Recommendation Engine

## Database

* MySQL

These communicate over a Docker network managed by Docker Compose.

---

# Dataset Source

The Indian Cars dataset is based on the publicly available specifications of Indian Cars on Kaggle:
* https://www.kaggle.com/datasets/abineshsaravanan/indian-cars-dataset

---

# Screenshots

*(Add screenshots of your application here inside a `Screenshots` folder)*

![Form Screenshot](Screenshots/1.png)
![Results Screenshot](Screenshots/2.png)
![Results Screenshot](Screenshots/3.png)

---

# Troubleshooting

## Docker won't start

```bash
docker compose down

docker compose up --build
```

---

## Port already in use

Change ports inside `docker-compose.yml` or stop the application currently using that port.

---

## Database connection error

Ensure:

* MySQL container is running
* Environment variables are correct
* Docker network is created successfully

---

# Author

**Akshat**

GitHub

https://github.com/akshats24

---

# Acknowledgements

Open-source technologies used:

* FastAPI
* React
* Docker
* MySQL
* SQLAlchemy
* Pydantic
* Pandas
* Axios
