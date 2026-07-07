import pandas as pd
from pathlib import Path
from sqlalchemy import inspect, text

from database import engine
from config import SCORE_WEIGHTS

THRESHOLD = 0.7
MILEAGE_PLACEHOLDER = 19.6

def get_budget_score(user_budget, min_price, max_price):
    """
    Calculates a budget compatibility score.
    Returns 1.0 if perfectly in budget, otherwise penalizes proportionally based on the gap.
    """
    if pd.isna(min_price) or pd.isna(max_price):
        return 0
    if min_price <= user_budget <= max_price:
        return 1.0
        
    gap = min(abs(user_budget - min_price), abs(user_budget - max_price))
    penalty = gap / max(user_budget, 1)
    
    return max(0, 1 - penalty)

def check_user_prefs(user_pref, car_pref_full):
    """
    Evaluates string-based preferences like fuel or transmission.
    Awards full points for exact matches and partial points for secondary options.
    """
    if pd.isna(car_pref_full) or pd.isna(user_pref):
        return 0.0
        
    car_lower = str(car_pref_full).lower()
    user_lower = str(user_pref).lower()
    
    if user_lower not in car_lower:
        return 0.0
    
    parts = []
    for p in car_lower.split('&'):
        parts.append(p.strip())
        
    """give partial credit if it's a secondary option"""
    if len(parts) > 0 and parts[0] == user_lower:
        return 1.0
        
    return 0.75

def get_body_score(user_body, car_body):
    """
    Evaluates body type compatibility.
    Returns 1.0 for an exact match, 0.0 otherwise.
    """
    if pd.isna(car_body) or pd.isna(user_body):
        return 0
    return 1.0 if user_body.lower() == str(car_body).lower() else 0.0

def get_mileage_score(user_min_mileage, car_avg_mileage):
    """
    Calculates the mileage score based on the user's minimum requirement.
    Returns 1.0 if the car's mileage meets or exceeds the requirement,
    and a proportional score if it falls short.
    """
    if pd.isna(car_avg_mileage):
        return 0.5
    if abs(car_avg_mileage - MILEAGE_PLACEHOLDER) < 0.01:
        return 0.5
    if user_min_mileage == 0:
        return 1.0
    if car_avg_mileage >= user_min_mileage:
        return 1.0
        
    return max(0, car_avg_mileage / max(user_min_mileage, 1))

def get_seating_score(user_seats, min_seats, max_seats):
    """
    Evaluates the seating capacity score.
    Returns 1.0 if the user's requirement falls within the car's seating capacity,
    0.75 if the car has more seats than required, and 0.0 if it has fewer.
    """
    if pd.isna(min_seats) or pd.isna(max_seats):
        return 0
    if min_seats <= user_seats <= max_seats:
        return 1.0
    if max_seats < user_seats:
        """too small"""
        return 0.0
    """seats more than needed but that's okay"""
    return 0.75

def get_safety_score(user_safety, car_safety):
    """
    Calculates the safety rating score based on the user's minimum requirement.
    Returns 1.0 if the car meets or exceeds the required safety rating,
    and a proportional score if it falls short.
    """
    if pd.isna(car_safety):
        return 0.5
    if car_safety >= user_safety:
        return 1.0
    return max(0, car_safety / max(user_safety, 1))

def make_reasons_list(prefs, car, scores):
    """
    Generates dynamic tags explaining why a specific vehicle was matched to the user
    based on parameter scores that passed the threshold.
    """
    reasons = []
    if scores['budget'] >= THRESHOLD:
        reasons.append("Fits Your Budget")
    if scores['fuel_type'] >= THRESHOLD:
        reasons.append(f"Fuel: {prefs['fuel_type']}")
    if scores['transmission'] >= THRESHOLD:
        reasons.append(f"Transmission: {prefs['transmission']}")
    if scores['body_type'] >= THRESHOLD:
        reasons.append(f"{car['Body_Type']} Body Style")
    if scores['seating'] >= THRESHOLD:
        reasons.append(f"{prefs['seating']} Seater Comfort")
    if scores['safety'] >= THRESHOLD:
        reasons.append(f"{car['Safety_Rating']} Star Safety Rated")
    if scores['mileage'] >= THRESHOLD:
        reasons.append("Good Mileage")
    return reasons

def mix_brands(ranked_df, top_n):
    """
    Enforces brand diversity in recommendations to prevent all top matches
    originating from a single manufacturer.
    """
    seen_brands = set()
    primary = []
    overflow = []
    
    for _, row in ranked_df.iterrows():
        brand = row['brand']
        if brand not in seen_brands:
            seen_brands.add(brand)
            primary.append(row)
        else:
            overflow.append(row)
            
        if len(primary) == top_n:
            break
            
    if len(primary) < top_n:
        needed = top_n - len(primary)
        primary.extend(overflow[:needed])
        
    return pd.DataFrame(primary)

def run_matching_engine(prefs, df, top_n=5):
    """
    Core recommendation logic that applies weighted scoring against user preferences.
    Filters hard constraints first, then evaluates matching scores for all parameters.
    """
    cars = df.copy()
    
    """filter out cars way too expensive or too small immediately"""
    budget_ceiling = prefs['budget'] * 1.3
    u_seats = prefs['seating']
    
    filtered_cars = cars[
        (cars['Price_Min_Lakh'] <= budget_ceiling) &
        (cars['Seating_Max'] >= u_seats) &
        (cars['Mileage_Avg_kmpl'] >= prefs['min_mileage'])
    ]
    
    if filtered_cars.empty:
        return pd.DataFrame(columns=[
            "brand", "model", "body_type", "price_range_lakh",
            "fuel_type", "transmission", "safety_rating",
            "match_percent", "match_reasons"
        ])
        
    results = []
    for _, car in filtered_cars.iterrows():
        scores = {
            'budget': get_budget_score(prefs['budget'], car['Price_Min_Lakh'], car['Price_Max_Lakh']),
            'fuel_type': check_user_prefs(prefs['fuel_type'], car['Fuel_Type_Full']),
            'transmission': check_user_prefs(prefs['transmission'], car['Transmission_Full']),
            'body_type': get_body_score(prefs['body_type'], car['Body_Type']),
            'seating': get_seating_score(prefs['seating'], car['Seating_Min'], car['Seating_Max']),
            'mileage': get_mileage_score(prefs['min_mileage'], car['Mileage_Avg_kmpl']),
            'safety': get_safety_score(prefs['min_safety'], car['Safety_Rating']),
        }
        
        """calculate total score based on config weights"""
        total_score = 0
        for key in SCORE_WEIGHTS:
            total_score += scores[key] * SCORE_WEIGHTS[key]
        
        """format engine spec safely"""
        engine_min = car.get('Engine_Min_CC', 0)
        engine_max = car.get('Engine_Max_CC', 0)
        engine_cc = "N/A"
        if not pd.isna(engine_min):
            if engine_min == engine_max or pd.isna(engine_max):
                engine_cc = f"{int(engine_min)} CC"
            else:
                engine_cc = f"{int(engine_min)} CC - {int(engine_max)} CC"
        
        """format mileage safely"""
        mil_min = car.get('Mileage_Min_kmpl', 0)
        mil_max = car.get('Mileage_Max_kmpl', 0)
        exact_mileage = "N/A"
        if not pd.isna(mil_min):
            if mil_min == mil_max or pd.isna(mil_max):
                exact_mileage = f"{mil_min} kmpl"
            else:
                exact_mileage = f"{mil_min} kmpl to {mil_max} kmpl"
        
        """format safety details"""
        safety_rating_val = car.get('Safety_Rating', 0)
        ncap_body = car.get('NCAP_Body', '')
        
        if pd.isna(safety_rating_val):
            safety_details = "Not Tested"
        else:
            safety_details = f"{int(safety_rating_val)} Stars"
            if pd.notna(ncap_body) and ncap_body != "":
                safety_details += f" ({ncap_body})"
        
        """format seating safely"""
        seat_max = car.get('Seating_Max', 0)
        seating_capacity = "N/A"
        if not pd.isna(seat_max):
            seating_capacity = f"{int(seat_max)} Seater"

        results.append({
            "brand":            car["Brand"],
            "model":            car["Model"],
            "body_type":        car["Body_Type"],
            "price_range_lakh": f"{car['Price_Min_Lakh']} - {car['Price_Max_Lakh']}",
            "fuel_type":        car["Fuel_Type_Full"],
            "transmission":     car["Transmission_Full"],
            "safety_rating":    0.0 if pd.isna(car["Safety_Rating"]) else float(car["Safety_Rating"]),
            "match_percent":    round(total_score * 100, 1),
            "match_reasons":    make_reasons_list(prefs, car, scores),
            "engine_cc":        engine_cc,
            "exact_mileage":    exact_mileage,
            "safety_details":   safety_details,
            "seating_capacity": seating_capacity,
            "ground_clearance": "N/A" if pd.isna(car.get("Ground_Clearance_mm")) else str(car.get("Ground_Clearance_mm")),
            "boot_space":       "N/A" if pd.isna(car.get("Boot_Space_Liters")) else str(car.get("Boot_Space_Liters")),
            "drive_type":       "N/A" if pd.isna(car.get("Drive_Type")) else str(car.get("Drive_Type")),
            "fuel_tank_capacity": "N/A" if pd.isna(car.get("Fuel_Tank_Capacity_Liters")) else str(car.get("Fuel_Tank_Capacity_Liters")),
        })
        
    """sort by highest match"""
    ranked = pd.DataFrame(results).sort_values(by="match_percent", ascending=False).reset_index(drop=True)
    return mix_brands(ranked, top_n)

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
            
        self.cars_df = pd.read_sql("SELECT * FROM cars", engine)

    def _needs_seeding(self):
        """
        Checks if the cars database table exists and contains records.
        Returns True if the database is empty and needs to be seeded from the CSV.
        """
        inspector = inspect(engine)
        if not inspector.has_table("cars"):
            return True
            
        with engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM cars")).scalar()
        return count == 0

    def _seed_database_from_csv(self):
        """
        Reads the initial car dataset from a CSV file and populates the database table.
        """
        csv_path = Path("/app") / "datasets" / "cars_in.csv"
        seed_df = pd.read_csv(csv_path)
        seed_df.to_sql(name="cars", con=engine, if_exists="replace", index=False)

    def recommend_cars(self, user_input):
        """
        Public endpoint to trigger the matching engine and return formatted dictionaries.
        """
        results = run_matching_engine(prefs=user_input, df=self.cars_df, top_n=5)
        return results.to_dict(orient="records")
