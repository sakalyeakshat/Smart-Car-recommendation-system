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
docker compose up --build
```

## Access the Application
Once the terminal shows that both the backend and frontend servers are running, open your web browser:
* Frontend UI: http://localhost:3000
* Backend API: http://localhost:8089
* Swagger Docs: http://localhost:8089/docs
* ReDoc Docs: http://localhost:8089/redoc

## Stopping & Resetting
To gracefully stop the application: Press Ctrl + C in the terminal where Docker is running, or run:
```bash
docker compose down
```

To perform a full hard reset: If you want to completely wipe the database and start from a completely clean slate (for example, to re-run the initialization script), use the -v flag to destroy the volumes before rebuilding:
```bash
docker compose down -v
docker compose up --build
```

## Running Without Docker (Alternative)

If you prefer to run the application locally without Docker, you will need **Python (3.13+)**, **Node.js (20+)**, and a running **MySQL** server on your machine.

### 1. Database Setup
1. Ensure your local MySQL server is running.
2. Log in to your MySQL terminal and create the database:
   ```sql
   CREATE DATABASE smart_car_recommendation_system;
   ```

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your database environment variables (if different from defaults):
   * `DB_USER` (Default: `root`)
   * `DB_PASSWORD` (Default: `root`)
   * `DB_HOST` (Default: `localhost`)
   * `DB_PORT` (Default: `3306`)
   * `DB_NAME` (Default: `smart_car_recommendation_system`)
5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install --legacy-peer-deps
   ```
3. Start the development server:
   ```bash
   npm start
   ```
   The React application will be available at http://localhost:3000.

## Troubleshooting

### Operating System Compatibility
The application has been fully tested and verified to run seamlessly on both **Windows (Docker Desktop / WSL2)** and **macOS (Apple Silicon M-series & Intel)**.

### Docker fails to start
Rebuild the containers:
```bash
docker compose down
docker compose up --build
```

### Port already in use (Port is already allocated)
If Docker Compose fails with a message like `Bind for 0.0.0.0:<PORT> failed: port is already allocated` (typically for port 3000, 8089, or 3308):

#### Step 1: Stop any lingering container runs
```bash
docker compose down
```

#### Step 2: Kill conflicting local background processes
Identify and terminate the process holding the port on your host system:
*   **On macOS / Linux:**
    ```bash
    # 1. Find the PID of the process using the port (e.g., for port 8089)
    sudo lsof -i :8089
    
    # 2. Terminate the process using the PID found
    kill -9 <PID>
    ```
*   **On Windows (PowerShell):**
    ```powershell
    # 1. Find the PID of the process using the port (e.g., for port 8089)
    Get-NetTCPConnection -LocalPort 8089 | Select-Object OwningProcess
    
    # 2. Terminate the process
    Stop-Process -Id <PID> -Force
    ```

#### Step 3: Change ports in compose configuration (Alternative)
*   You can edit the external port mappings under `ports` in `docker-compose.yml` (e.g. changing `"8089:8000"` to `"8099:8000"`) and restart the container.

## Environment Variables
Note: When running with Docker, you do not need to manually create any .env files. All necessary development environment variables (like database credentials and ports) are safely handled and injected directly via the docker-compose.yml file. If running without Docker, you can set these variables in your shell environment.
