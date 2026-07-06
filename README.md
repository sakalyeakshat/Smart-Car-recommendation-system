🚗 DriveMatch AI
Python FastAPI React MySQL Docker

📖 Project Overview
DriveMatch AI is a Smart Car Recommendation System that generates personalized car recommendations based on a user's preferences.

Users provide information such as:

Budget
Fuel Type
Transmission
Body Type
Seating Capacity
Minimum Mileage
Minimum Safety Rating
Based on these inputs, the application recommends the best-matching cars using a weighted recommendation engine backed by a MySQL database.

The project demonstrates the use of modern full-stack development technologies by combining a React frontend, FastAPI backend, MySQL database, and Docker containerization into a scalable recommendation system.

🎯 Why I Chose This Project
I chose to develop a Smart Car Recommendation System because buying a car is a decision most people struggle with, comparing endless options across budget, fuel type, safety, and seating without any clear way to weigh them together.

This application acts as a personal car advisor, scoring every car in the database against a user's preferences and showing the best matches instead of a generic list.

This project allowed me to build a practical recommendation system while applying concepts from full-stack development, REST API development, database management, and Docker containerization. It also provided an opportunity to integrate multiple technologies into a complete production-like application.

⭐ What Makes This Project Special
Unlike simple filter-based car search tools that just list every match, DriveMatch AI generates ranked recommendations based on multiple user-specific parameters that actually have significance in determining the right car.

DriveMatch AI considers:

Budget
Fuel Type
Transmission
Body Type
Seating Capacity
Mileage
Safety Rating
✨ Features
Personalized car recommendations
FastAPI REST API
React frontend
MySQL database
Dockerized architecture
Docker Compose support
Responsive user interface
Input validation using Pydantic
Automatic API documentation
Weighted scoring recommendation engine
Brand diversity pass on results
🛠 Technology Stack
Backend
Python
FastAPI
SQLAlchemy
Pydantic
Uvicorn
PyMySQL
Pandas
Frontend
React
CSS
Database
MySQL
DevOps
Docker
Docker Compose
Development Tools
Visual Studio Code
Git
GitHub
🏗 Project Architecture
                    User
                      │
                      ▼
               React Frontend
                      │
             REST API Requests
                      │
                      ▼
              FastAPI Backend
                      │
            Recommendation Engine
                      │
                      ▼
               MySQL Database
📂 Project Structure
Smart-Car-recommendation-system/
│
├── backend/
│   ├── app/
│   │     ├── main.py
│   │     ├── config.py
│   │     ├── recommendation/
│   │     │        └── recommend.py
│   │     ├── routers/
│   │     ├── schemas/
│   │     └── services/
│   ├── database/
│   ├── datasets/
│   ├── dockerfile
│   ├── requirements.txt
│   └── start.sh
│
├── frontend/
│   ├── src/
│   │     ├── App.js
│   │     ├── components/
│   │     └── styles/
│   ├── public/
│   ├── dockerfile
│   └── package.json
│
├── mysql/
│   └── init.sql
│
├── screenshort/
│
└── docker-compose.yml
⚙️ How To Install
Prerequisites
Install the following software:

Git
Docker Desktop (includes Docker Compose)
Verify installation:

docker --version
docker compose version
Clone the Repository
git clone https://github.com/sakalyeakshat/Smart-Car-recommendation-system.git

cd Smart-Car-recommendation-system
🚀 Running with Docker (Recommended)
Build and start all services:

docker compose up
To rebuild after changes:

docker compose up --build
Run in detached mode:

docker compose up -d
Stop containers:

docker compose down
Remove containers and volumes:

docker compose down -v
🌐 Application URLs
Frontend

http://localhost:3000
Backend API

http://localhost:8000
Swagger Documentation

http://localhost:8000/docs
ReDoc Documentation

http://localhost:8000/redoc
💻 Running Without Docker
Backend
Create a virtual environment

python -m venv venv
Activate it

Windows

venv\Scripts\activate
Linux/macOS

source venv/bin/activate
Install dependencies

pip install -r requirements.txt
Run the backend

uvicorn app.main:app --reload
Frontend
Install dependencies

npm install
Run React

npm start
🗄 Database Setup
The application uses MySQL.

When Docker Compose is executed:

MySQL container starts automatically.
Database and cars table are created automatically.
Backend waits for MySQL to be healthy, then starts.
Dataset is auto-seeded into MySQL on first run.
No manual database setup is required.

🚀 How To Use
Start the application using Docker Compose.

Open your browser.

http://localhost:3000
Fill in the vehicle preferences form.
Enter:

Budget
Fuel Type
Transmission
Body Type
Seating Capacity
Minimum Mileage
Minimum Safety Rating
Click the Find Best Matches button.

The React frontend sends your preferences to the FastAPI backend.

The backend validates the request using Pydantic.

The recommendation engine scores cars from the MySQL database according to the user's preferences.

The top matching cars are ranked, with a brand diversity pass applied.

The personalized car recommendations are displayed on the screen.

To test the backend directly, open:

http://localhost:8000/docs
Swagger UI allows testing every endpoint without using the frontend.

⚙️ How the Recommendation Engine Works
User submits vehicle preferences.
FastAPI validates incoming data.
Recommendation engine loads car data from MySQL.
Cars are filtered according to:
Budget Range
Seating Requirement
Remaining cars are scored according to:
Budget
Fuel Type
Transmission
Safety Rating
Body Type
Seating
Mileage
Results are ranked and passed through a brand diversity pass.
Results are returned as JSON.
React displays the car recommendations.
👤 User Inputs
The recommendation engine considers:

Budget
Fuel Type
Transmission
Body Type
Seating Capacity
Mileage
Safety Rating
These inputs allow the system to generate personalized car recommendations instead of displaying a generic, unranked list.

🗄 Dataset Preparation & Preprocessing
The application uses an Indian Cars Dataset obtained from Kaggle.

Before importing the dataset into MySQL, several preprocessing steps were performed to improve consistency and usability.

Data Cleaning
Removed duplicate records.
Removed incomplete or invalid entries.
Removed unnecessary columns.
Cleaned whitespace and null values.
Data Structuring
Organized the cleaned data into a relational MySQL table.
Verified data integrity before importing.
Documented exploration and cleaning steps in a notebook.
Since this project uses a rule-based weighted recommendation system rather than machine learning, no feature engineering or model training was required.

✔ Validation
The backend validates all requests using Pydantic.

Examples include:

Missing fields
Invalid values
Incorrect data types
Empty requests
Appropriate HTTP status codes are returned whenever validation fails.

🐳 Docker Architecture
The project consists of three independent containers.

Frontend
React
Backend
FastAPI
Recommendation Engine
Database
MySQL
Docker Compose automatically creates the network and allows communication between all containers.

📊 Dataset Source
Dataset used:

Indian Cars Dataset

Source:

https://www.kaggle.com

The dataset was cleaned and transformed before being imported into MySQL.

📸 Screenshots
Home Page
![Home Page](screenshort/HomePage.png)

Vehicle Preferences Form
![Form](screenshort/Form.png)

Car Recommendations
![Recommendation](screenshort/RecommendationPage.png)

Explore More
![Explore More](screenshort/ExploreMore.png)

🔮 Future Improvements
User authentication
Saved searches
AI-powered recommendations
EMI calculator
Comparison view
Dealer locator
Cloud deployment
Mobile application
🛠 Troubleshooting
Docker won't start
docker compose down

docker compose up --build
Port already in use
Modify the ports inside:

docker-compose.yml
or stop the application using the conflicting port.

Database connection error
Ensure:

MySQL container is running
Docker network is created successfully
Database credentials are correct
Backend starts after MySQL initialization
👨‍💻 Author
Akshat Sakalye

GitHub:

https://github.com/sakalyeakshat

🙏 Acknowledgements
This project was developed as part of a technical recruitment assessment.

Open-source technologies used:

FastAPI
React
Docker
MySQL
SQLAlchemy
Pydantic
Pandas
Special thanks to the open-source community and Kaggle for providing the dataset used in this project.
