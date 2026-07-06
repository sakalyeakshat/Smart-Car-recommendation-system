import pandas as pd
from pathlib import Path
from sqlalchemy import inspect

from database.database import engine
from app.recommendation.recommend import get_top_recommendations


class RecommendationService:

    def __init__(self):
        # seed from CSV if the table got wiped (e.g. fresh docker volume)
        if not inspect(engine).has_table("cars"):
            self._seed_database_from_csv()

        self.cars_df = pd.read_sql("SELECT * FROM cars", engine)
        print(f"Loaded {len(self.cars_df)} cars from MySQL.")

    def _seed_database_from_csv(self):
        base_dir = Path("/app")
        csv_path = base_dir / "datasets" / "raw" / "cars_in.csv"
        seed_df = pd.read_csv(csv_path)
        seed_df.to_sql(name="cars", con=engine, if_exists="replace", index=False)
        print(f"Seeded {len(seed_df)} cars into MySQL from backup CSV.")

    def recommend_cars(self, user_input):
        results = get_top_recommendations(prefs=user_input, df=self.cars_df, top_n=5)
        return results.to_dict(orient="records")