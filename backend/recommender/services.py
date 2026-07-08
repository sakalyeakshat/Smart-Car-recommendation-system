"""
Recommendation service layer.
Exposes the RecommendationService class that coordinates engine logic and DB access.
"""
import pandas as pd
from pathlib import Path
from sqlalchemy import inspect, text

from database import engine as db_engine
from recommender.engine import run_matching_engine

class RecommendationService:
    def __init__(self):
        self._wait_for_db()
        """setup db if not seeded yet"""
        if self._needs_seeding():
            print("seeding database from csv...")
            self._seed_database_from_csv()
            
        self.cars_df = pd.read_sql("SELECT * FROM cars", db_engine)

    def _wait_for_db(self):
        import time
        from sqlalchemy import text
        print("Waiting for database connection...")
        for i in range(30):
            try:
                with db_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                print("Database connection established!")
                return
            except Exception:
                print(f"Database not ready yet (attempt {i+1}/30), retrying in 2s...")
                time.sleep(2)
        print("ERROR: Database connection timed out. Exiting.")
        raise RuntimeError("Database connection timed out")

    def _needs_seeding(self):
        inspector = inspect(db_engine)
        if not inspector.has_table("cars"):
            return True
            
        with db_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM cars")).scalar()
        return count == 0

    def _seed_database_from_csv(self):
        csv_path = Path("/app") / "datasets" / "cars_in.csv"
        seed_df = pd.read_csv(csv_path)
        seed_df.to_sql(name="cars", con=db_engine, if_exists="replace", index=False)

    def recommend_cars(self, user_input):
        results = run_matching_engine(prefs=user_input, df=self.cars_df, top_n=5)
        return results.to_dict(orient="records")
