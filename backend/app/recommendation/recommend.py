"""
recommend.py

Core recommendation engine for DriveMatch AI.
"""

import pandas as pd
from pathlib import Path


# -----------------------------
# WEIGHTS (no change)
# -----------------------------
SCORE_WEIGHTS = {
    'budget': 0.30,
    'fuel_type': 0.20,
    'transmission': 0.15,
    'safety': 0.15,
    'body_type': 0.10,
    'seating': 0.05,
    'mileage': 0.05,
}


# -----------------------------
# DATA LOADING (FIXED FOR DOCKER)
# -----------------------------
def load_car_data(csv_file_path=None):
    """
    Loads dataset safely in both local + Docker environments.
    """

    # If path is given, use it
    if csv_file_path is not None:
        return pd.read_csv(csv_file_path)

    # Docker-safe fallback path
    base_path = Path("/app")  # WORKDIR in Docker
    csv_path = base_path / "datasets" / "raw" / "cars_in.csv"

    return pd.read_csv(csv_path)


# -----------------------------
# SCORING FUNCTIONS (UNCHANGED)
# -----------------------------
def calculate_budget_score(user_budget_lakh, car_min_price, car_max_price):
    if pd.isna(car_min_price) or pd.isna(car_max_price):
        return 0
    if car_min_price <= user_budget_lakh <= car_max_price:
        return 1.0
    gap = min(abs(user_budget_lakh - car_min_price), abs(user_budget_lakh - car_max_price))
    penalty = gap / max(user_budget_lakh, 1)
    return max(0, 1 - penalty)


def calculate_match_score(user_choice, car_options_text):
    if pd.isna(car_options_text) or pd.isna(user_choice):
        return 0
    return 1.0 if user_choice.lower() in str(car_options_text).lower() else 0.0


def calculate_body_type_score(user_body_type, car_body_type):
    if pd.isna(car_body_type) or pd.isna(user_body_type):
        return 0
    return 1.0 if user_body_type.lower() == str(car_body_type).lower() else 0.0


def calculate_mileage_score(user_min_mileage, car_avg_mileage):
    if pd.isna(car_avg_mileage):
        return 0
    if car_avg_mileage >= user_min_mileage:
        return 1.0
    return max(0, car_avg_mileage / user_min_mileage)


def calculate_seating_score(user_seats_needed, car_min_seats, car_max_seats):
    if pd.isna(car_min_seats) or pd.isna(car_max_seats):
        return 0
    if car_min_seats <= user_seats_needed <= car_max_seats:
        return 1.0
    return 0.5 if abs(user_seats_needed - car_max_seats) <= 2 else 0.0


def calculate_safety_score(user_min_safety_stars, car_safety_rating):
    if pd.isna(car_safety_rating):
        return 0.5
    if car_safety_rating >= user_min_safety_stars:
        return 1.0
    return max(0, car_safety_rating / max(user_min_safety_stars, 1))


# -----------------------------
# REASONS (UNCHANGED)
# -----------------------------
def build_match_reasons(user_preferences, car, scores):
    reasons = []
    REASON_THRESHOLD = 0.7

    if scores['budget'] >= REASON_THRESHOLD:
        reasons.append("Within Budget")
    if scores['fuel_type'] >= REASON_THRESHOLD:
        reasons.append(user_preferences['fuel_type'])
    if scores['transmission'] >= REASON_THRESHOLD:
        reasons.append(user_preferences['transmission'])
    if scores['body_type'] >= REASON_THRESHOLD:
        reasons.append(f"{car['Body_Type']} Body Type")
    if scores['seating'] >= REASON_THRESHOLD:
        reasons.append(f"{user_preferences['seating']} Seater")
    if scores['safety'] >= REASON_THRESHOLD and not pd.isna(car['Safety_Rating']):
        reasons.append(f"{int(car['Safety_Rating'])} Star Safety")
    if scores['mileage'] >= REASON_THRESHOLD:
        reasons.append("Good Mileage")

    return reasons


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def get_top_recommendations(user_preferences, car_dataframe, number_of_results=5):

    scored_cars = []

    for _, car in car_dataframe.iterrows():

        scores = {
            'budget': calculate_budget_score(
                user_preferences['budget'],
                car['Price_Min_Lakh'],
                car['Price_Max_Lakh']
            ),
            'fuel_type': calculate_match_score(
                user_preferences['fuel_type'],
                car['Fuel_Type_Full']
            ),
            'transmission': calculate_match_score(
                user_preferences['transmission'],
                car['Transmission_Full']
            ),
            'body_type': calculate_body_type_score(
                user_preferences['body_type'],
                car['Body_Type']
            ),
            'seating': calculate_seating_score(
                user_preferences['seating'],
                car['Seating_Min'],
                car['Seating_Max']
            ),
            'mileage': calculate_mileage_score(
                user_preferences['min_mileage'],
                car['Mileage_Avg_kmpl']
            ),
            'safety': calculate_safety_score(
                user_preferences['min_safety'],
                car['Safety_Rating']
            ),
        }

        final_score = sum(scores[k] * SCORE_WEIGHTS[k] for k in SCORE_WEIGHTS)
        match_reasons = build_match_reasons(user_preferences, car, scores)

        scored_cars.append({
            'Brand': car['Brand'],
            'Model': car['Model'],
            'Body_Type': car['Body_Type'],
            'Price_Range_Lakh': f"{car['Price_Min_Lakh']}-{car['Price_Max_Lakh']}",
            'Match_Percent': round(final_score * 100, 1),
            'Fuel_Type': car['Fuel_Type_Full'],
            'Transmission': car['Transmission_Full'],
            'Safety_Rating': car['Safety_Rating'],
            'Match_Reasons': match_reasons,
        })

    results = pd.DataFrame(scored_cars).sort_values(
        'Match_Percent',
        ascending=False
    )

    return results.head(number_of_results)