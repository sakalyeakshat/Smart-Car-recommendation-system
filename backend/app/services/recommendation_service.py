
import pandas as pd
from pathlib import Path
from sqlalchemy import inspect
 
from database.database import engine
from app.recommendation.recommend import get_top_recommendations
 
 
class RecommendationService:
 
    def __init__(self):
 
        print("Checking if 'cars' table exists in MySQL...")
 
        # If the table is missing (e.g. after a fresh/reset database volume),
        # automatically load it from the CSV backup instead of crashing.
        # This makes the app self-healing across container restarts.
        if not inspect(engine).has_table("cars"):
            print("'cars' table not found - seeding from CSV backup...")
            self._seed_database_from_csv()
 
        print("Loading cars from MySQL...")
        self.cars_df = pd.read_sql("SELECT * FROM cars", engine)
        print(f"Loaded {len(self.cars_df)} cars from MySQL.")
 
    def _seed_database_from_csv(self):
        base_dir = Path("/app")
        csv_path = base_dir / "datasets" / "raw" / "cars_in.csv"
        seed_df = pd.read_csv(csv_path)
        seed_df.to_sql(name="cars", con=engine, if_exists="replace", index=False)
        print(f"Seeded {len(seed_df)} cars into MySQL from backup CSV.")
 
    def recommend_cars(self, user_input):
        recommendations = get_top_recommendations(
            user_preferences=user_input,
            car_dataframe=self.cars_df,
            number_of_results=5,
        )
        return recommendations.to_dict(orient="records")