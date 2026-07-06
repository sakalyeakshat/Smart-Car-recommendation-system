# DriveMatch AI — Smart Car Recommendation System

A fully containerised, plug-and-play car recommendation web application that matches users to the best-fitting vehicles based on their budget, fuel preference, body type, seating needs, mileage expectation, and safety requirements.

---

## Why This Project?

Buying a car is one of the most significant purchasing decisions a person makes, yet most people spend hours manually filtering through hundreds of models across dozens of websites — only to end up confused.

**DriveMatch AI** solves this by acting as a personal car advisor: the user fills in a simple preference form, and the system instantly scores every car in the database against those preferences using a weighted multi-criteria algorithm, then returns the top 5 best-matching vehicles with a human-readable explanation of *why* each car was recommended.

What makes it special:
- **Weighted scoring engine** — each preference dimension (budget, fuel, transmission, safety, body type, seating, mileage) carries a tuned weight, so more important factors have a stronger influence on results.
- **Brand diversity pass** — the algorithm ensures results span different manufacturers, so users are not shown five Maruti cars when many other brands also match well.
- **Explore More feature** — each recommended car has an "Explore More" modal that explains the car's specific strengths and trade-offs (e.g. "CNG is significantly cheaper per km than petrol or diesel", "CNG cylinder occupies boot space").
- **Fully plug-and-play** — one command (`docker compose up`) brings up all three containers with zero manual setup.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vanilla CSS |
| Backend / API | Python 3.10, FastAPI, Uvicorn |
| Database | MySQL 8.0 (via Docker) |
| ORM / Data | SQLAlchemy 2, Pandas |
| Containerisation | Docker, Docker Compose |
| Data Source | Indian Cars dataset (Kaggle — `cars_in.csv`) |

---

## Project Structure

```
Smart-Car-recommendation-system/
│
├── backend/
│   ├── app/
│   │   ├── main.py                        # FastAPI app entry point, CORS, routers
│   │   ├── config.py                      # Centralised algorithm constants
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
│   │   └── explore_and_clean.ipynb        # Data exploration notebook
│   ├── dockerfile
│   ├── requirements.txt
│   └── start.sh                           # MySQL readiness poll + uvicorn start
│
├── frontend/
│   ├── public/
│   │   └── index.html                     # HTML shell with app title and meta
│   ├── src/
│   │   ├── App.js                         # Root component, state, routing logic
│   │   ├── components/
│   │   │   ├── Hero.jsx                   # Landing hero banner
│   │   │   ├── RecommendationPage.jsx     # Preference input form
│   │   │   ├── ResultsPage.jsx            # Results layout (best + others)
│   │   │   ├── CarCard.jsx                # Individual car result card
│   │   │   ├── ExploreModal.jsx           # Strengths/considerations modal
│   │   │   └── Services.jsx               # Feature highlights section
│   │   └── styles/                        # Per-component CSS files
│   ├── dockerfile
│   └── package.json
│
├── mysql/
│   └── init.sql                           # Schema creation (auto-run by MySQL on first boot)
│
└── docker-compose.yml                     # Orchestrates all three containers
```

---

## Architecture

```
Browser (localhost:3000)
        |
        v
 +--------------+      React dev-server proxy       +-----------------+
 |   Frontend   | ---- /recommend, /explore ------> |    Backend      |
 |  (React 19)  | <--- JSON response --------------- |   (FastAPI)     |
 +--------------+                                    +--------+--------+
                                                              | SQLAlchemy
                                                              v
                                                    +-----------------+
                                                    |   MySQL 8.0     |
                                                    |  (cars table)   |
                                                    +-----------------+

All three services run on a custom Docker bridge network: app_network
```

---

## How the Recommendation Algorithm Works

### 1. Pre-filter (hard constraints)
Cars that cannot physically meet requirements are excluded entirely:
- `Price_Min_Lakh <= budget * 1.3` (30% ceiling for near-budget cars)
- `Seating_Max >= requested_seats` (a 5-seater cannot carry 7 people)

### 2. Weighted scoring
Each remaining car is scored on 7 dimensions:

| Dimension | Weight | Scoring Logic |
|---|---|---|
| Budget | 30% | Proportional penalty for deviation from range |
| Fuel Type | 20% | Full score for exact match, 0.75 for multi-fuel |
| Transmission | 15% | Full score for exact match, 0.75 for multi-tx |
| Safety Rating | 15% | Proportional to how close it is to user's minimum |
| Body Type | 10% | Binary exact match |
| Seating | 5% | Full score if within range, 0.75 if car has more seats |
| Mileage | 5% | Proportional, neutral (0.5) for missing/placeholder data |

### 3. Brand diversity pass
Results are sorted by score descending, then a greedy selection ensures at most one car per brand fills the top-N slots — preventing any one brand from dominating the list.

---

## API Reference

### `POST /recommend`
Returns the top 5 car recommendations for a given set of preferences.

**Request body:**
```json
{
  "budget": 10,
  "fuel_type": "Petrol",
  "transmission": "Manual",
  "body_type": "Hatchback",
  "seating": 5,
  "min_mileage": 15,
  "min_safety": 3
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "brand": "Maruti",
      "model": "Swift",
      "body_type": "Hatchback",
      "price_range_lakh": "6.49 - 9.64",
      "fuel_type": "Petrol",
      "transmission": "Manual & Automatic",
      "safety_rating": 3.0,
      "match_percent": 91.5,
      "match_reasons": ["Fits Your Budget", "Fuel: Petrol", "Hatchback Body Style"]
    }
  ]
}
```

### `POST /explore`
Returns key strengths and things to consider for a specific car.

**Request body:**
```json
{
  "fuel_type": "Petrol",
  "transmission": "Manual",
  "body_type": "Hatchback"
}
```

**Response:**
```json
{
  "key_strengths": [
    "Easy to manoeuvre and park in tight city spaces.",
    "More driver control with better fuel efficiency.",
    "Smooth and refined petrol engine for everyday driving."
  ],
  "things_to_consider": [
    "Smaller boot space compared to sedans and SUVs.",
    "Constant clutch use can be tiring in heavy stop-go traffic.",
    "Running costs add up faster on long daily highway commutes."
  ]
}
```

---

## Data Source & Preparation

- **Source**: Indian car market dataset downloaded from [Kaggle](https://www.kaggle.com)
- **File**: `backend/datasets/raw/cars_in.csv`
- **Exploration**: `backend/datasets/explore_and_clean.ipynb` documents the data exploration steps, column selection rationale, and any cleaning applied before the CSV was used.

Key columns used:
`Brand`, `Model`, `Body_Type`, `Price_Min_Lakh`, `Price_Max_Lakh`, `Fuel_Type_Full`, `Transmission_Full`, `Seating_Min`, `Seating_Max`, `Mileage_Avg_kmpl`, `Safety_Rating`

### Auto-seeding
On first run, if the `cars` table is empty, the backend automatically reads `cars_in.csv` and seeds it into MySQL via `pandas.to_sql()`. No manual database setup is ever required.

---

## Running the Project

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### One-command startup
```bash
git clone https://github.com/<your-username>/Smart-Car-recommendation-system.git
cd Smart-Car-recommendation-system
docker compose up
```

Then open **http://localhost:3000** in your browser.

### What happens on `docker compose up`
1. **MySQL** starts and `init.sql` runs automatically, creating the `cars` table
2. **Backend** waits for MySQL to be healthy, then starts FastAPI and auto-seeds the CSV data into the database
3. **Frontend** starts the React dev server on port 3000
4. The app is fully ready with no manual steps needed

### Stopping
```bash
docker compose down
```

To also remove the database volume for a completely fresh start:
```bash
docker compose down -v
```

---

## Container Configuration

| Container | Base Image | Internal Port | Host Port | Network |
|---|---|---|---|---|
| `mysql_db` | `mysql:8.0` | 3306 | 3307 | app_network |
| `fastapi_backend` | `python:3.10` | 8000 | 8000 | app_network |
| `react_frontend` | `node:20-alpine` | 3000 | 3000 | app_network |

All containers communicate over the custom bridge network `app_network`. The frontend's React dev-server proxy routes all API calls (`/recommend`, `/explore`) to `fastapi_backend:8000` — keeping API communication internal to the Docker network.

---

## License

MIT License — see [LICENSE](./LICENSE) for details.
