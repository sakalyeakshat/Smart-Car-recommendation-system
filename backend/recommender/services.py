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
    """
    Service class handling recommendation business logic and data access.
    Manages database initialization and exposes methods to retrieve car recommendations.
    """
    def __init__(self):
        """
        Initializes the service by ensuring the database is seeded with initial data
        and loading the cars dataset into memory.
        """
        """setup db if not seeded yet"""
        if self._needs_seeding():
            print("seeding database from csv...")
            self._seed_database_from_csv()
            
        self.cars_df = pd.read_sql("SELECT * FROM cars", db_engine)

    def _needs_seeding(self):
        """
        Checks if the cars database table exists and contains records.
        Returns True if the database is empty and needs to be seeded from the CSV.
        """
        inspector = inspect(db_engine)
        if not inspector.has_table("cars"):
            return True
            
        with db_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM cars")).scalar()
        return count == 0

    def _seed_database_from_csv(self):
        """
        Reads the initial car dataset from a CSV file and populates the database table.
        """
        csv_path = Path("/app") / "datasets" / "cars_in.csv"
        seed_df = pd.read_csv(csv_path)
        seed_df.to_sql(name="cars", con=db_engine, if_exists="replace", index=False)

    def recommend_cars(self, user_input):
        """
        Public endpoint to trigger the matching engine and return formatted dictionaries.
        """
        results = run_matching_engine(prefs=user_input, df=self.cars_df, top_n=5)
        return results.to_dict(orient="records")
