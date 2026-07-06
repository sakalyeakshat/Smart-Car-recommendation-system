import pandas as pd
from pathlib import Path
from sqlalchemy import inspect, text

from database.database import engine
from app.recommendation.recommend import get_top_recommendations


class RecommendationService:

    def __init__(self):
        # Seed from CSV if the table is empty or doesn't exist yet
        if self._needs_seeding():
            self._seed_database_from_csv()
        self.cars_df = pd.read_sql("SELECT * FROM cars", engine)

    def _needs_seeding(self):
        inspector = inspect(engine)
        if not inspector.has_table("cars"):
            return True
        with engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM cars")).scalar()
        return count == 0

    def _seed_database_from_csv(self):
        csv_path = Path("/app") / "datasets" / "raw" / "cars_in.csv"
        seed_df = pd.read_csv(csv_path)
        seed_df.to_sql(name="cars", con=engine, if_exists="replace", index=False)

    def recommend_cars(self, user_input):
        results = get_top_recommendations(prefs=user_input, df=self.cars_df, top_n=5)
        return results.to_dict(orient="records")