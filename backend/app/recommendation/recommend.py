import pandas as pd
from app.config import SCORE_WEIGHTS

# Min score for a criteria to be listed in match_reasons
THRESHOLD = 0.7

# ~80% of CSV rows have this mileage value — it means "no data"
MILEAGE_PLACEHOLDER = 19.6


def calculate_budget_score(user_budget, min_price, max_price):
    if pd.isna(min_price) or pd.isna(max_price):
        return 0
    if min_price <= user_budget <= max_price:
        return 1.0
    gap = min(abs(user_budget - min_price), abs(user_budget - max_price))
    penalty = gap / max(user_budget, 1)
    return max(0, 1 - penalty)


def calculate_fuel_score(user_fuel, car_fuel_full):
    """Partial credit when the car supports the user's fuel alongside others."""
    if pd.isna(car_fuel_full) or pd.isna(user_fuel):
        return 0
    car_lower = str(car_fuel_full).lower()
    user_lower = user_fuel.lower()
    if user_lower not in car_lower:
        return 0.0
    parts = [p.strip() for p in car_lower.split('&')]
    return 1.0 if parts[0] == user_lower else 0.75


def calculate_transmission_score(user_tx, car_tx_full):
    """Partial credit for multi-transmission cars so they aren't penalised to zero."""
    if pd.isna(car_tx_full) or pd.isna(user_tx):
        return 0
    car_lower = str(car_tx_full).lower()
    user_lower = user_tx.lower()
    if user_lower not in car_lower:
        return 0.0
    parts = [p.strip() for p in car_lower.split('&')]
    return 1.0 if parts[0] == user_lower else 0.75


def calculate_body_type_score(user_body, car_body):
    if pd.isna(car_body) or pd.isna(user_body):
        return 0
    return 1.0 if user_body.lower() == str(car_body).lower() else 0.0


def calculate_mileage_score(user_min_mileage, car_avg_mileage):
    if pd.isna(car_avg_mileage):
        return 0.5
    if abs(car_avg_mileage - MILEAGE_PLACEHOLDER) < 0.01:
        return 0.5
    if user_min_mileage == 0:
        return 1.0
    if car_avg_mileage >= user_min_mileage:
        return 1.0
    return max(0, car_avg_mileage / max(user_min_mileage, 1))


def calculate_seating_score(user_seats, min_seats, max_seats):
    if pd.isna(min_seats) or pd.isna(max_seats):
        return 0
    if min_seats <= user_seats <= max_seats:
        return 1.0
    if max_seats < user_seats:
        return 0.0
    return 0.75


def calculate_safety_score(user_safety, car_safety):
    if pd.isna(car_safety):
        return 0.5
    if car_safety >= user_safety:
        return 1.0
    return max(0, car_safety / max(user_safety, 1))


def build_match_reasons(prefs, car, scores):
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


def apply_brand_diversity(ranked_df, top_n):
    """
    Pick the top-scoring car from each brand first, then fill remaining
    slots with the best leftover cars if there aren't enough distinct brands.
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


def get_top_recommendations(prefs, df, top_n=5):
    cars = df.copy()

    # Hard filter — budget ceiling and seating are non-negotiable
    budget_ceiling = prefs['budget'] * 1.3
    user_seats = prefs['seating']

    filtered = cars[
        (cars['Price_Min_Lakh'] <= budget_ceiling) &
        (cars['Seating_Max'] >= user_seats)
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
                prefs['budget'], car['Price_Min_Lakh'], car['Price_Max_Lakh']
            ),
            'fuel_type': calculate_fuel_score(
                prefs['fuel_type'], car['Fuel_Type_Full']
            ),
            'transmission': calculate_transmission_score(
                prefs['transmission'], car['Transmission_Full']
            ),
            'body_type': calculate_body_type_score(
                prefs['body_type'], car['Body_Type']
            ),
            'seating': calculate_seating_score(
                prefs['seating'], car['Seating_Min'], car['Seating_Max']
            ),
            'mileage': calculate_mileage_score(
                prefs['min_mileage'], car['Mileage_Avg_kmpl']
            ),
            'safety': calculate_safety_score(
                prefs['min_safety'], car['Safety_Rating']
            ),
        }

        score = sum(scores[key] * SCORE_WEIGHTS[key] for key in SCORE_WEIGHTS)

        results.append({
            "brand":            car["Brand"],
            "model":            car["Model"],
            "body_type":        car["Body_Type"],
            "price_range_lakh": f"{car['Price_Min_Lakh']} - {car['Price_Max_Lakh']}",
            "fuel_type":        car["Fuel_Type_Full"],
            "transmission":     car["Transmission_Full"],
            "safety_rating":    0.0 if pd.isna(car["Safety_Rating"]) else float(car["Safety_Rating"]),
            "match_percent":    round(score * 100, 1),
            "match_reasons":    build_match_reasons(prefs, car, scores),
        })

    ranked = (
        pd.DataFrame(results)
        .sort_values(by="match_percent", ascending=False)
        .reset_index(drop=True)
    )

    return apply_brand_diversity(ranked, top_n)