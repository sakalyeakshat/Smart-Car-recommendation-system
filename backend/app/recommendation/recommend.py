import pandas as pd

# weights tuned after a few test runs — budget matters most
SCORE_WEIGHTS = {
    'budget':       0.30,
    'fuel_type':    0.20,
    'transmission': 0.15,
    'safety':       0.15,
    'body_type':    0.10,
    'seating':      0.05,
    'mileage':      0.05,
}

THRESHOLD = 0.7

# Placeholder mileage value used for ~80 % of rows in the CSV.
# Treat it as "data unavailable" — give a neutral 0.5 so it doesn't
# unfairly reward or punish those cars.
MILEAGE_PLACEHOLDER = 19.6


# ── individual scorers ────────────────────────────────────────────────────────

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


def calculate_fuel_score(user_fuel, car_fuel_full):
    """Partial credit when the car supports the user's fuel type alongside others."""
    if pd.isna(car_fuel_full) or pd.isna(user_fuel):
        return 0
    car_lower = str(car_fuel_full).lower()
    user_lower = user_fuel.lower()
    if user_lower not in car_lower:
        return 0.0
    # Full score only when it is the primary / sole fuel type
    # (i.e. the user fuel appears first or the string is exactly it)
    parts = [p.strip() for p in car_lower.split('&')]
    return 1.0 if parts[0] == user_lower else 0.75


def calculate_transmission_score(user_tx, car_tx_full):
    """
    Partial credit for 'Manual & Automatic' when user asks for Manual,
    so a car that supports both isn't penalised to zero.
    """
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
        return 0.5                          # unknown → neutral
    if abs(car_avg_mileage - MILEAGE_PLACEHOLDER) < 0.01:
        return 0.5                          # placeholder → neutral
    if user_min_mileage == 0:
        return 1.0                          # user has no mileage requirement
    if car_avg_mileage >= user_min_mileage:
        return 1.0
    return max(0, car_avg_mileage / max(user_min_mileage, 1))


def calculate_seating_score(user_seats, min_seats, max_seats):
    if pd.isna(min_seats) or pd.isna(max_seats):
        return 0
    if min_seats <= user_seats <= max_seats:
        return 1.0
    # A car with fewer seats than required cannot physically fit the user's
    # group — no partial credit. Only give partial credit when the car has
    # MORE seats than requested (e.g. user wants 5, car offers 7).
    if max_seats < user_seats:
        return 0.0
    return 0.75  # car has more seats than needed — good but not perfect


def calculate_safety_score(user_safety, car_safety):
    if pd.isna(car_safety):
        return 0.5                          # unknown → neutral
    if car_safety >= user_safety:
        return 1.0
    return max(0, car_safety / max(user_safety, 1))


# ── match-reason builder ──────────────────────────────────────────────────────

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


# ── brand-diversity pass ──────────────────────────────────────────────────────

def apply_brand_diversity(ranked_df, top_n):
    """
    Greedy selection that prefers one car per brand.

    Pass 1 — walk the score-sorted list and pick the highest-scoring
              car from each brand until we have top_n results.
    Pass 2 — if fewer than top_n unique brands exist, fill remaining
              slots with the best-scoring cars that were skipped.

    This guarantees the output is always diverse when the data allows
    it, while never producing fewer than top_n results unnecessarily.
    """
    seen_brands = set()
    primary = []     # one winner per brand
    overflow = []    # runner-up / duplicate-brand cars

    for _, row in ranked_df.iterrows():
        brand = row['brand']
        if brand not in seen_brands:
            seen_brands.add(brand)
            primary.append(row)
        else:
            overflow.append(row)

        if len(primary) == top_n:
            break

    # If not enough distinct brands, pad with the best-scored duplicates
    if len(primary) < top_n:
        needed = top_n - len(primary)
        primary.extend(overflow[:needed])

    return pd.DataFrame(primary)


# ── main entry point ──────────────────────────────────────────────────────────

def get_top_recommendations(prefs, df, top_n=5):
    cars = df.copy()

    # ── pre-filter ────────────────────────────────────────────────────────────
    # Hard-filter on budget (30 % ceiling) and seating capacity.
    # Seating is a hard physical constraint — a 5-seater cannot carry 7
    # people, so cars with insufficient max seats are excluded entirely
    # rather than scored down. Body type, fuel, and transmission are left
    # to the weighted scorer so rare combinations still surface results.
    budget_ceiling = prefs['budget'] * 1.3
    user_seats    = prefs['seating']

    filtered = cars[
        (cars['Price_Min_Lakh'] <= budget_ceiling) &
        (cars['Seating_Max']    >= user_seats)
    ]

    if filtered.empty:
        return pd.DataFrame(columns=[
            "brand", "model", "body_type", "price_range_lakh",
            "fuel_type", "transmission", "safety_rating",
            "match_percent", "match_reasons"
        ])

    # ── score every candidate ─────────────────────────────────────────────────
    results = []

    for _, car in filtered.iterrows():
        scores = {
            'budget': calculate_budget_score(
                prefs['budget'],
                car['Price_Min_Lakh'],
                car['Price_Max_Lakh']
            ),
            'fuel_type': calculate_fuel_score(
                prefs['fuel_type'],
                car['Fuel_Type_Full']
            ),
            'transmission': calculate_transmission_score(
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
            "brand":            car["Brand"],
            "model":            car["Model"],
            "body_type":        car["Body_Type"],
            "price_range_lakh": f"{car['Price_Min_Lakh']} - {car['Price_Max_Lakh']}",
            "fuel_type":        car["Fuel_Type_Full"],
            "transmission":     car["Transmission_Full"],
            "safety_rating":    car["Safety_Rating"],
            "match_percent":    round(score * 100, 1),
            "match_reasons":    build_match_reasons(prefs, car, scores),
        })

    # ── rank then diversify ───────────────────────────────────────────────────
    # Sort all candidates by score descending, then run the brand-diversity
    # pass so the top-N results always span different manufacturers where
    # possible — prevents e.g. all 5 slots being Maruti cars.
    ranked = (
        pd.DataFrame(results)
        .sort_values(by="match_percent", ascending=False)
        .reset_index(drop=True)
    )

    return apply_brand_diversity(ranked, top_n)