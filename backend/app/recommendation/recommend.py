import pandas as pd

# weights tuned after a few test runs — budget matters most
SCORE_WEIGHTS = {
    'budget': 0.30,
    'fuel_type': 0.20,
    'transmission': 0.15,
    'safety': 0.15,
    'body_type': 0.10,
    'seating': 0.05,
    'mileage': 0.05,
}


def load_car_data(file_path):  # unused — data comes from MySQL now
    return pd.read_csv(file_path)


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


def build_match_reasons(prefs, car, scores):
    reasons = []
    THRESHOLD = 0.7

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


def get_top_recommendations(prefs, df, top_n=5):
    cars = df.copy()

    filtered = cars[
        (cars['Price_Min_Lakh'] <= prefs['budget']) &
        (cars['Body_Type'].str.lower() == prefs['body_type'].lower()) &
        (cars['Fuel_Type_Full'].str.lower().str.contains(prefs['fuel_type'].lower()))
    ]

    if filtered.empty:
        return pd.DataFrame(columns=[
            "brand", "model", "body_type", "price_range_lakh",
            "fuel_type", "transmission", "safety_rating",
            "match_percent", "match_reasons"
        ])

    results = []

    for _, car in filtered.iterrows():
        scores = {
            'budget': calculate_budget_score(
                prefs['budget'],
                car['Price_Min_Lakh'],
                car['Price_Max_Lakh']
            ),
            'fuel_type': calculate_match_score(
                prefs['fuel_type'],
                car['Fuel_Type_Full']
            ),
            'transmission': calculate_match_score(
                prefs['transmission'],
                car['Transmission_Full']
            ),
            'body_type': calculate_body_type_score(
                prefs['body_type'],
                car['Body_Type']
            ),
            'seating': calculate_seating_score(
                prefs['seating'],
                car['Seating_Min'],
                car['Seating_Max']
            ),
            'mileage': calculate_mileage_score(
                prefs['min_mileage'],
                car['Mileage_Avg_kmpl']
            ),
            'safety': calculate_safety_score(
                prefs['min_safety'],
                car['Safety_Rating']
            ),
        }

        score = sum(
            scores[key] * SCORE_WEIGHTS[key]
            for key in SCORE_WEIGHTS
        )

        results.append({
            "brand": car["Brand"],
            "model": car["Model"],
            "body_type": car["Body_Type"],
            "price_range_lakh": f"{car['Price_Min_Lakh']} - {car['Price_Max_Lakh']}",
            "fuel_type": car["Fuel_Type_Full"],
            "transmission": car["Transmission_Full"],
            "safety_rating": car["Safety_Rating"],
            "match_percent": round(score * 100, 1),
            "match_reasons": build_match_reasons(prefs, car, scores)
        })

    ranked = pd.DataFrame(results)
    return ranked.sort_values(
        by="match_percent",
        ascending=False
    ).head(top_n)