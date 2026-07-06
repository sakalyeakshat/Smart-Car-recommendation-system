import os
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

DB_USERNAME = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")  # docker-compose overrides this
DB_PORT = os.getenv("DB_PORT", "3307")
DB_NAME = os.getenv("DB_NAME", "smart_car_recommendation_system")

engine = create_engine(
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "datasets" / "raw" / "cars_in.csv"

print("CSV Path:", csv_path)

df = pd.read_csv(csv_path)
print(f"Cars found in CSV: {len(df)}")

df.to_sql(
    name="cars",
    con=engine,
    if_exists="replace",
    index=False
)

print("✅ Cars imported successfully!")