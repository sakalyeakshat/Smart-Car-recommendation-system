import pandas as pd

# -----------------------------
# SCORING WEIGHTS
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
# LOAD DATA (FROM CSV)
# -----------------------------
def load_car_data(file_path):
    return pd.read_csv(file_path)


# -----------------------------
# SCORING FUNCTIONS
# -----------------------------
def calculate_budget_score(user_budget, min_price, max_price):
    if pd.isna(min_price) or pd.isna(max_price):
        return 0

    if min_price <= user_budget <= max_price:
        return 1.0

    gap = min(
        abs(user_budget - min_price),
        abs(user_budget - max_price)
    )

    penalty = gap / max(user_budget, 1)
    return max(0, 1 - penalty)


def calculate_match_score(user_choice, car_text):
    if pd.isna(car_text) or pd.isna(user_choice):
        return 0
    return 1.0 if user_choice.lower() in str(car_text).lower() else 0.0


def calculate_body_type_score(user_body, car_body):
    if pd.isna(car_body) or pd.isna(user_body):
        return 0
    return 1.0 if user_body.lower() == str(car_body).lower() else 0.0


def calculate_mileage_score(user_min_mileage, car_avg_mileage):
    if pd.isna(car_avg_mileage):
        return 0
    if car_avg_mileage >= user_min_mileage:
        return 1.0
    return max(0, car_avg_mileage / max(user_min_mileage, 1))


def calculate_seating_score(user_seats, min_seats, max_seats):
    if pd.isna(min_seats) or pd.isna(max_seats):
        return 0
    if min_seats <= user_seats <= max_seats:
        return 1.0
    return 0.5 if abs(user_seats - max_seats) <= 2 else 0.0


def calculate_safety_score(user_safety, car_safety):
    if pd.isna(car_safety):
        return 0.5
    if car_safety >= user_safety:
        return 1.0
    return max(0, car_safety / max(user_safety, 1))


# -----------------------------
# MATCH REASONS
# -----------------------------
def build_match_reasons(user_preferences, car, scores):
    reasons = []
    THRESHOLD = 0.7

    if scores['budget'] >= THRESHOLD:
        reasons.append("Fits Your Budget")

    if scores['fuel_type'] >= THRESHOLD:
        reasons.append(f"Fuel: {user_preferences['fuel_type']}")

    if scores['transmission'] >= THRESHOLD:
        reasons.append(f"Transmission: {user_preferences['transmission']}")

    if scores['body_type'] >= THRESHOLD:
        reasons.append(f"{car['Body_Type']} Body Style")

    if scores['seating'] >= THRESHOLD:
        reasons.append(f"{user_preferences['seating']} Seater Comfort")

    if scores['safety'] >= THRESHOLD:
        reasons.append(f"{car['Safety_Rating']} Star Safety Rated")

    if scores['mileage'] >= THRESHOLD:
        reasons.append("Good Mileage")

    return reasons


# -----------------------------
# MAIN FUNCTION (API SAFE)
# -----------------------------
def get_top_recommendations(user_preferences, car_dataframe, number_of_results=5):

    cars = car_dataframe.copy()

    # ---------------- FILTERS ----------------
    filtered = cars[
        (cars['Price_Min_Lakh'] <= user_preferences['budget']) &
        (cars['Body_Type'].str.lower() == user_preferences['body_type'].lower()) &
        (cars['Fuel_Type_Full'].str.lower().str.contains(user_preferences['fuel_type'].lower()))
    ]

    if filtered.empty:
        return pd.DataFrame(columns=[
            "brand",
            "model",
            "body_type",
            "price_range_lakh",
            "fuel_type",
            "transmission",
            "safety_rating",
            "match_percent",
            "match_reasons"
        ])

    results = []

    # ---------------- SCORING ----------------
    for _, car in filtered.iterrows():

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

        final_score = sum(
            scores[key] * SCORE_WEIGHTS[key]
            for key in SCORE_WEIGHTS
        )

        # ✅ FINAL API RESPONSE FORMAT (IMPORTANT FIX)
        results.append({
            "brand": car["Brand"],
            "model": car["Model"],
            "body_type": car["Body_Type"],
            "price_range_lakh": f"{car['Price_Min_Lakh']} - {car['Price_Max_Lakh']}",
            "fuel_type": car["Fuel_Type_Full"],
            "transmission": car["Transmission_Full"],
            "safety_rating": car["Safety_Rating"],
            "match_percent": round(final_score * 100, 1),
            "match_reasons": build_match_reasons(user_preferences, car, scores)
        })

    output = pd.DataFrame(results)

    return output.sort_values(
        by="match_percent",
        ascending=False
    ).head(number_of_results)