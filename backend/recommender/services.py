"""Service layer for database checking, data seeding, and matching queries."""

import pandas as pd
from pathlib import Path
from sqlalchemy import inspect, text
from database import engine as db_engine
from recommender.engine import run_matching_engine

class RecommendationService:
    """Manages database initialization, data seeding, and matching queries."""

    def __init__(self):
        """Connect to MySQL database, run seeding migrations, and load cars into memory."""
        self._wait_for_db()
        if self._needs_seeding():
            print("seeding database...")
            self._seed_db_records()
        self.cars_df = pd.read_sql("SELECT * FROM cars", db_engine)

    def _wait_for_db(self):
        """Wait for database server connection to become available."""
        import time
        from sqlalchemy import text
        print("Waiting for database connection...")
        for i in range(30):
            try:
                with db_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                print("Database ready!")
                return
            except Exception:
                print(f"Database not ready yet (attempt {i+1}/30), waiting...")
                time.sleep(2)
        print("Database timed out.")
        raise RuntimeError("Database connection timed out")

    def _needs_seeding(self):
        """Verify database tables check and confirm if records or columns are missing."""
        inspector = inspect(db_engine)
        if not inspector.has_table("cars"):
            return True
            
        columns = [col['name'] for col in inspector.get_columns("cars")]
        if "Range_km" not in columns:
            return True
            
        with db_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM cars")).scalar()
        return count == 0

    def _seed_db_records(self):
        """Load and import car records from CSV dataset into MySQL table."""
        csv_path = Path(__file__).resolve().parents[1] / "datasets" / "cars_in.csv"
        df = pd.read_csv(csv_path)
        df.to_sql(name="cars", con=db_engine, if_exists="replace", index=False)

    def get_recommendations(self, user_input):
        """Generate and format top ranked vehicle recommendations based on preferences."""
        results = run_matching_engine(prefs=user_input, df=self.cars_df, top_n=5)
        return results.to_dict(orient="records")
