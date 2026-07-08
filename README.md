# Smart-Car-recommendation-System

## Project Overview
Smart-Car-recommendation-System is a Smart Car Recommendation System that generates personalized vehicle suggestions based on a user's profile, budget, and driving preferences.

Users provide information such as:
* Budget (in Lakhs)
* Fuel Type preference
* Transmission preference
* Body Type preference
* Minimum passenger seating capacity
* Minimum required mileage (kmpl)
* Minimum crash safety rating (stars)

Based on these inputs, the application recommends optimized car matches using a weighted multi-criteria scoring algorithm backed by a MySQL database.

The project demonstrates the use of modern full-stack development technologies by combining a React frontend, FastAPI backend, MySQL database, and Docker containerization into a scalable recommendation system.

## Why I Chose This Project
Car purchasing is often an overwhelming decision involving multiple trade-offs (e.g., budget vs. safety, mileage vs. performance). A Recommendation System solves this real-world problem by acting as an unbiased digital advisor.

I wanted to build something that doesn't just blindly filter data. This application uses a weighted scoring algorithm to find the closest matches even if a car isn't a 100% perfect fit for every single parameter. It also enforces brand diversity so users aren't flooded with recommendations from just one manufacturer, and provides dynamic key strengths to help users make informed decisions.

This project allowed me to build a practical recommendation system while applying concepts from full-stack development, database management and Docker containerization. It also provided an opportunity to integrate multiple technologies into a complete production-like application.

## What Makes This Project Special
Unlike traditional car-buying search tools that perform rigid matching, this system dynamically scores vehicle compatibility across multiple parameters that actually matter to buyers.

The system evaluates:
* Budget proximity and price boundaries
* Primary and secondary fuel capabilities
* Gearbox availability
* Body design configurations
* Seating capacity requirements
* Proportional safety ratings
* Proportional mileage scores

The software generates multiple recommendations sorted by match percentage, and the user can click "Explore More" on any car to inspect complete technical specifications.

## Documentation
Detailed documentation has been split into separate files for easier navigation:

* [Installation Guide](INSTALL.md)
* [Usage Guide](USAGE.md)
* [API Documentation](API_DOCUMENT.md)

## System Architecture

The application follows a containerized three-tier architecture (Frontend, Backend, Database) connected through a custom Docker bridge network.

```text
                     User
                       │
                       ▼
                 React Frontend
                       │
             HTTP REST API Requests
                       │
                       ▼
                FastAPI Backend
                       │
              Request Validation
                  (Pydantic)
                       │
                       ▼
         Weighted Recommendation Engine
                       │
             SQLAlchemy + Pandas
                       │
                       ▼
                MySQL Database
```

### Component Overview
* **Frontend (React)**: Collects user preferences through questionnaire inputs, sends API calls using Axios, and visualizes the recommendations.
* **Backend (FastAPI)**: Validates incoming payloads using Pydantic, queries database tables, runs the weighted matching algorithm, and caches the active database dataset into an in-memory Pandas DataFrame on startup for rapid retrieval.
* **Database (MySQL)**: Standardizes car records and specs. Automatically initialized and seeded via `db/init.sql` and the backend service.

### Recommendation Logic
1. **Pre-Filtering (Hard Constraints)**: Instantly prunes cars that exceed 130% of the user's budget, have fewer seats than requested, or fall short of the minimum mileage.
2. **Weighted Scoring**: Evaluates and scores similarity (0.0 to 1.0) on remaining cars. Attributes are weighted based on buyer priorities: Budget (30%), Fuel Type (20%), Transmission (15%), Safety (15%), Body Style (10%), Seating (5%), and Mileage (5%).
3. **Brand Diversity**: Prevents a single manufacturer from dominating recommendations by ensuring the top recommendations represent up to 5 unique brands.
4. **Explanation Badges**: Appends reason tags (e.g. "Fits Your Budget", "5 Star Safety Rated") for attributes scoring $\ge 0.7$.

### Data Flow
User Form Submission $\to$ React Axios POST $\to$ FastAPI Endpoints $\to$ Pydantic Validation $\to$ Recommendation Engine (Filters, Similarity, Weights, Brand Diversity) $\to$ JSON Response $\to$ React Recommendation Card Display.

## Features
* Personalized car recommendations with explanation badges
* Brand diversity filtering to ensure a variety of choices
* Explore More details listing key strengths and technical specifications
* Weighted multi-criteria scoring engine
* Input validation using Pydantic
* Fully containerized application using Docker
* Clean, responsive, modern user interface

## Technology Stack

### Backend
* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn
* PyMySQL
* Pandas

### Frontend
* React
* Axios
* CSS

### Database
* MySQL

### DevOps
* Docker
* Docker Compose

### Development Tools
* Visual Studio Code
* Git
* GitHub

## Project Structure
```text
Smart-Car-recommendation-system/
│
├── db/
│   └── init.sql
│
├── backend/
│   ├── datasets/
│   │   └── cars_in.csv
│   ├── recommender/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   └── services.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── recommend.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── request.py
│   │   └── response.py
│   ├── config.py
│   ├── database.py
│   ├── dockerfile
│   ├── requirements.txt
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ExploreModal.jsx
│   │   │   ├── RecommendationForm.jsx
│   │   │   ├── ResultsPage.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── Footer.jsx
│   │   ├── styles/
│   │   │   ├── Navbar.css
│   │   │   └── Footer.css
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── index.js
│   ├── public/
│   ├── dockerfile
│   └── package.json
│
├── docker-compose.yml
├── README.md
├── INSTALL.md
├── USAGE.md
├── API_DOCUMENT.md
└── LICENSE
```

## Application URLs
* **Frontend**: http://localhost:3000
* **Backend API**: http://localhost:8000
* **Swagger Documentation**: http://localhost:8000/docs

## Dataset Source
* **Kaggle Source**: [Indian Cars under 20 Lakhs](https://www.kaggle.com/datasets/shiivvvaam/indian-cars-under-20-lakhs)
* **Status**: Cleaned missing values, normalized engine sizes, and manually enriched specifications (ground clearance, boot space, drive type, fuel tank capacity, and NCAP body specifications) for complete matching.
* **Logo Source**: Icons obtained from [Icons8](https://icons8.com/icons/set/favicon-car--static).

## Screenshots

### Home Page
![Home Page](Screenshots/HomePage.png)

### User Request Form
![Form Screenshot](Screenshots/Form.png)

### Recommendation Cards
![Recommendation Cards](Screenshots/RecommendationCards.png)

### Explore More
![Explore More](Screenshots/Explore.png)

## Future Improvements
* User authentication and favorite selections profile
* Compare side-by-side specs of multiple matches
* Real-time price tracking and notifications
* Native mobile applications
* Cloud deployment on AWS/GCP

## Author
* **sakalyeakshat**
* GitHub: https://github.com/sakalyeakshat

## Acknowledgements
Open-source technologies used: FastAPI, React, Docker, MySQL, SQLAlchemy, Pydantic, Pandas, Axios. Special thanks to Kaggle for the raw dataset and Icons8 for graphics.

## AI Declaration
To be fully transparent, I have used Claude/AI coding tools to help speed up some of the repetitive tasks in this project:
* **Debugging Windows line-ending conflicts**: Restructuring the wait loops and handling container carriage-return issues on Windows host volume mounts.
* **Data Preprocessing & Enrichment**: Helping automate formatting scripts to clean missing values and normalize CC ranges in `cars_in.csv`.
* **Proofreading**: Checking grammar and formatting structure of the technical docs and comments.

Aside from that, the rules of recommendation, the dataset enrichment, the React components, and the Docker network structures were built by me.

