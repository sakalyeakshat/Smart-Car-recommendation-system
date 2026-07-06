🚗 DriveMatch AI
Python FastAPI React MySQL Docker

📖 Project Overview
DriveMatch AI is a car recommendation system I built to help people figure out which car actually suits them, based on their budget, fuel preference, transmission choice, body type, seating needs, mileage expectation, and safety requirements.

You give it a few basic inputs:

Budget (₹ Lakh)
Fuel Type
Transmission
Body Type
Seating Capacity
Minimum Mileage
Minimum Safety Rating
and it scores every car in the database against those preferences using a weighted recommendation engine, then hands you back the ones that fit best, backed by a MySQL database.

It's a full-stack project — React on the frontend, FastAPI on the backend, MySQL for storage, and the whole thing runs in Docker so anyone can spin it up with one command.

🎯 Why I Built This
I built DriveMatch AI because buying a car is genuinely one of the more stressful purchases people make. You end up with fifteen browser tabs open, comparing specs across different sites, and somehow still feel unsure by the end of it.

Most people don't really know how to weigh budget against fuel type against safety against seating all at once — everything matters a little, but nothing gets prioritized properly. I wanted to build something that does that weighing for you and actually tells you why a car showed up as a match.

This project also gave me a good excuse to practice full-stack development end to end — building a real REST API, designing a database around messy real-world data, and packaging everything with Docker so it isn't a pain to run.

⭐ What Makes This Different
A lot of car-search tools are really just filters — they show you everything that technically matches and let you sort through it yourself. DriveMatch AI instead scores and ranks cars using a weighted system, so the "best" match is actually the best match, not just one option among fifty.

Here's what it factors in:

Budget
Fuel Type
Transmission
Body Type
Seating Capacity
Mileage
Safety Rating
A few things I focused on while building it:

Weighted scoring engine — every factor (budget, fuel, transmission, safety, body type, seating, mileage) has its own weight, so the things that matter more actually count for more in the final score.
Brand diversity pass — without this, the top results tend to get dominated by whichever brand happens to have the most models that fit. I added a pass that spreads the recommendations across different manufacturers.
Explore More — each recommended car comes with a quick breakdown of its actual strengths and trade-offs, not just a match percentage.
Zero manual setup — one docker compose up and all three services (frontend, backend, database) come up and talk to each other automatically.
✨ Features
Personalized car recommendations
FastAPI REST API
React frontend
MySQL database
Dockerized, one-command setup
Docker Compose support
Responsive UI
Input validation using Pydantic
Auto-generated API docs
Weighted multi-criteria recommendation engine
Brand diversity pass on results
Dataset auto-seeds into MySQL on first run
🛠 Tech Stack
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
Vanilla CSS
Database
MySQL
DevOps
Docker
Docker Compose
Tools
Visual Studio Code
Git
GitHub
🏗 Architecture
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
│   │   ├── main.py                        # FastAPI app entry point, CORS, routers
│   │   ├── config.py                      # Scoring weights and algorithm constants
│   │   ├── recommendation/
│   │   │   └── recommend.py               # Core weighted scoring engine
│   │   ├── routers/
│   │   │   ├── recommendation.py          # POST /recommend endpoint
│   │   │   └── explore.py                 # POST /explore endpoint
│   │   ├── schemas/
│   │   │   ├── request.py                 # Pydantic input model
│   │   │   ├── response.py                # Pydantic output model
│   │   │   └── explore.py                 # Pydantic explore models
│   │   └── services/
│   │       └── recommendation_service.py  # DB seeding + query logic
│   ├── database/
│   │   └── database.py                    # SQLAlchemy engine setup
│   ├── datasets/
│   │   ├── raw/
│   │   │   └── cars_in.csv                # Source dataset (Kaggle)
│   │   └── explore_and_clean.ipynb        # Data exploration + cleaning notes
│   ├── dockerfile
│   ├── requirements.txt
│   └── start.sh                           # Waits for MySQL, then starts uvicorn
│
├── frontend/
│   ├── public/
│   │     └── index.html
│   ├── src/
│   │     ├── App.js
│   │     ├── components/
│   │     └── styles/
│   ├── dockerfile
│   └── package.json
│
├── mysql/
│   └── init.sql
│
├── screenshort/
│
└── docker-compose.yml
⚙️ Getting Set Up
What you'll need
Git
Docker Desktop (comes with Docker Compose)
Check they're installed:

docker --version
docker compose version
Clone it
git clone https://github.com/sakalyeakshat/Smart-Car-recommendation-system.git

cd Smart-Car-recommendation-system
🚀 Running with Docker (the easy way)
Bring everything up:

docker compose up
Rebuild after making changes:

docker compose up --build
Run it in the background:

docker compose up -d
Stop everything:

docker compose down
Stop and wipe the database too:

docker compose down -v
🌐 Where to Find Things
Frontend

http://localhost:3000
Backend API

http://localhost:8000
Swagger docs

http://localhost:8000/docs
ReDoc docs

http://localhost:8000/redoc
💻 Running It Without Docker
Backend
Set up a virtual environment

python -m venv venv
Activate it

Windows

venv\Scripts\activate
Linux/macOS

source venv/bin/activate
Install the dependencies

pip install -r requirements.txt
Start the backend

uvicorn app.main:app --reload
Frontend
Install packages

npm install
Start React

npm start
🗄 Database Setup
No manual setup needed here — MySQL handles itself when you run Docker Compose:

The MySQL container starts up.
init.sql runs automatically and creates the cars table.
The backend waits until MySQL is actually healthy before it starts (see start.sh).
If the cars table is empty, the backend reads cars_in.csv and seeds it straight into MySQL using pandas.to_sql().
That's it — no scripts to run by hand.

🚀 How to Use It
Start everything with Docker Compose.

Open your browser and go to:

http://localhost:3000
Fill in your preferences:

Budget (₹ Lakh)
Fuel Type
Transmission
Body Type
Seating Capacity
Minimum Mileage
Minimum Safety Rating
Hit Find Best Matches.

From there:

The frontend sends your preferences to the FastAPI backend.
Pydantic validates the request.
The recommendation engine scores every car in the database against what you asked for.
The best matches are picked, ranked, and passed through the brand diversity check.
You get back a ranked list of cars, each with an Explore More option that breaks down its strengths and trade-offs.
If you want to poke at the API directly, head to:

http://localhost:8000/docs
The Swagger UI lets you test every endpoint without touching the frontend at all.

⚙️ How the Recommendation Engine Actually Works
Preferences come in from the frontend.
FastAPI validates the request.
The engine pulls car data from MySQL.
A pre-filter step drops cars that just can't work, regardless of score:
Price_Min_Lakh <= budget * 1.3 (a bit of headroom above the stated budget)
Seating_Max >= requested_seats (no point suggesting a 5-seater to someone who needs 7)
Whatever's left gets scored across 7 weighted factors:
Factor	Weight	How it's scored
Budget	30%	Penalized proportionally the further a car sits from your range
Fuel Type	20%	Full marks for an exact match, partial credit for multi-fuel cars
Transmission	15%	Same idea — exact match scores highest, multi-transmission gets partial credit
Safety Rating	15%	Scored by how close it is to your minimum requirement
Body Type	10%	Exact match or nothing
Seating	5%	Full score if it fits, slightly reduced if the car seats more than you need
Mileage	5%	Proportional, with a neutral score when the data is missing
Everything gets sorted by score, then the brand diversity pass kicks in so one manufacturer doesn't hog every top spot.
The top 5 go back as JSON.
React renders them, with the Explore More view available for each one.
👤 What It Asks For
The engine factors in:

Budget
Fuel Type
Transmission
Body Type
Seating Capacity
Mileage
Safety Rating
This is really the whole point of the project — instead of one generic list of cars, everyone gets a ranking that actually reflects what they said mattered to them.

🗄 Dataset & Cleanup
The dataset is an Indian car market dataset from Kaggle.

Before it went anywhere near MySQL, I cleaned it up a fair bit:

Cleaning
Dropped duplicate records.
Removed incomplete or clearly invalid rows.
Cleaned up stray whitespace and null values.
Standardized how fuel type, transmission, and body type were labeled.
Structuring
Mapped the cleaned data into a proper relational table (cars) in MySQL.
Double-checked data integrity before importing anything.
Documented the exploration and column choices in explore_and_clean.ipynb.
Since this is a rule-based, weighted-scoring system and not a machine learning model, there was no training or feature engineering involved — just careful data prep.

Columns actually used: Brand, Model, Body_Type, Price_Min_Lakh, Price_Max_Lakh, Fuel_Type_Full, Transmission_Full, Seating_Min, Seating_Max, Mileage_Avg_kmpl, Safety_Rating.

✔ Validation
Every request gets validated by Pydantic before it touches the recommendation engine — missing fields, invalid values, wrong data types, empty requests, all of it. If something's off, you get a proper HTTP error back instead of a silent failure.

🐳 Docker Setup
Three containers, each doing its own job:

Frontend — React
Backend — FastAPI + the recommendation engine
Database — MySQL
Container	Base Image	Internal Port	Host Port
mysql_db	mysql:8.0	3306	3307
fastapi_backend	python:3.10	8000	8000
react_frontend	node:20-alpine	3000	3000
Docker Compose wires them all together on a shared bridge network, app_network, so they can talk to each other without any extra config.

📊 Where the Data Came From
Dataset: Indian Cars Dataset

Source: Kaggle (cars_in.csv)

Cleaned and restructured before it went into MySQL — see the Dataset & Cleanup section above for details.

📸 Screenshots
### Home Page
![Home Page](Smart-Car-recommendation-system/screenshort/HomePage.png)

### Vehicle Preferences Form
![Vehicle Preferences Form](Smart-Car-recommendation-system/screenshort/Form.png)

### Car Recommendations
![Car Recommendations](Smart-Car-recommendation-system/screenshort/RecommendationPage.png)

### Explore More
![Explore More](Smart-Car-recommendation-system/screenshort/ExploreMore.png)

🔮 What's Next
User authentication
Saved searches / favourites
Price trends and depreciation insights
AI-powered recommendations
EMI and affordability calculator
Side-by-side comparison of shortlisted cars
Dealer locator
Cloud deployment
Mobile app
🛠 Troubleshooting
Docker won't start
docker compose down

docker compose up --build
Port already taken
Change the ports in docker-compose.yml, or stop whatever else is using them.

Database connection errors
Check that:

The MySQL container is actually running
Docker's network got created properly
The DB credentials match what's in docker-compose.yml
The backend is starting after MySQL, not before (start.sh handles this)
👨‍💻 Author
Akshat Sakalye

GitHub: https://github.com/sakalyeakshat

🙏 Acknowledgements
This project was built as part of a technical recruitment assessment.

Built with these open-source tools:

FastAPI
React
Docker
MySQL
SQLAlchemy
Pydantic
Pandas
Thanks to the open-source community, and to Kaggle for the dataset this project runs on.