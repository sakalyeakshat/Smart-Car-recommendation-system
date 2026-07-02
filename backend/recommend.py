"""
recommend.py

This file contains the core logic for DriveMatch AI's recommendation engine.
Given a user's preferences (budget, fuel type, body type, etc.), it scores
every car in the dataset and returns the top matches, along with the specific
reasons each car was recommended.

How scoring works:
Each preference gets its own "score" between 0 and 1 (0 = no match, 1 = perfect match).
Then all scores are combined using weighted percentages (defined in SCORE_WEIGHTS below),
so more important preferences (like budget) count for more than less important ones.
"""

import pandas as pd


# How much each factor counts toward the final match score.
# Body Type was added after review feedback - since it's a meaningful preference
# for buyers, mileage and seating weights were each trimmed slightly to make room
# for it, keeping the total at 100%.
SCORE_WEIGHTS = {
    'budget': 0.30,
    'fuel_type': 0.20,
    'transmission': 0.15,
    'safety': 0.15,
    'body_type': 0.10,
    'seating': 0.05,
    'mileage': 0.05,
}


def load_car_data(csv_file_path):
    """Reads the cleaned car dataset from CSV into a pandas DataFrame."""
    return pd.read_csv(csv_file_path)


def calculate_budget_score(user_budget_lakh, car_min_price, car_max_price):
    """
    Checks how well a car's price range fits the user's stated budget.
    Full score (1.0) if the budget falls inside the car's price range.
    Partial score if it's close but outside the range.
    """
    if pd.isna(car_min_price) or pd.isna(car_max_price):
        return 0
    if car_min_price <= user_budget_lakh <= car_max_price:
        return 1.0
    gap = min(abs(user_budget_lakh - car_min_price), abs(user_budget_lakh - car_max_price))
    penalty = gap / max(user_budget_lakh, 1)
    return max(0, 1 - penalty)


def calculate_match_score(user_choice, car_options_text):
    """
    Used for Fuel Type and Transmission.
    Some cars support multiple options (e.g. "Petrol & CNG"), so this checks
    if the user's chosen option appears anywhere in the car's available options.
    """
    if pd.isna(car_options_text) or pd.isna(user_choice):
        return 0
    return 1.0 if user_choice.lower() in str(car_options_text).lower() else 0.0


def calculate_body_type_score(user_body_type, car_body_type):
    """
    Checks if the car's body type (SUV, Sedan, Hatchback, MUV/MPV, etc.)
    matches what the user asked for. This is a simple exact match since
    body type is a clear-cut preference, not a range.
    """
    if pd.isna(car_body_type) or pd.isna(user_body_type):
        return 0
    return 1.0 if user_body_type.lower() == str(car_body_type).lower() else 0.0


def calculate_mileage_score(user_min_mileage, car_avg_mileage):
    """
    Rewards cars that meet or exceed the mileage the user wants.
    Cars below the requirement get a proportional partial score instead of zero,
    since a slightly lower mileage shouldn't fully disqualify a car.
    """
    if pd.isna(car_avg_mileage):
        return 0
    if car_avg_mileage >= user_min_mileage:
        return 1.0
    return max(0, car_avg_mileage / user_min_mileage)


def calculate_seating_score(user_seats_needed, car_min_seats, car_max_seats):
    """
    Checks if the car's seating range covers what the user needs.
    Gives half credit if it's close (within 2 seats) rather than a hard cutoff.
    """
    if pd.isna(car_min_seats) or pd.isna(car_max_seats):
        return 0
    if car_min_seats <= user_seats_needed <= car_max_seats:
        return 1.0
    return 0.5 if abs(user_seats_needed - car_max_seats) <= 2 else 0.0


def calculate_safety_score(user_min_safety_stars, car_safety_rating):
    """
    Compares car's safety star rating against the user's minimum requirement.
    Cars with no safety data get a neutral 0.5 instead of being penalized
    unfairly for missing information.
    """
    if pd.isna(car_safety_rating):
        return 0.5
    if car_safety_rating >= user_min_safety_stars:
        return 1.0
    return max(0, car_safety_rating / max(user_min_safety_stars, 1))


def build_match_reasons(user_preferences, car, scores):
    """
    Builds a human-readable list of reasons explaining why this car was
    recommended, based on which individual criteria scored well.
    This is what gets shown to the user under "Why This Car?" in the UI.
    A criterion is only listed as a reason if it scored reasonably well
    (0.7 or higher) - low-scoring criteria are left out rather than shown
    as a false positive.
    """
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


def get_top_recommendations(user_preferences, car_dataframe, number_of_results=5):
    """
    Main function: scores every car against the user's preferences,
    combines the individual scores using SCORE_WEIGHTS, and returns
    the highest-scoring cars along with the specific reasons each was matched.
    """
    scored_cars = []

    for _, car in car_dataframe.iterrows():
        scores = {
            'budget': calculate_budget_score(
                user_preferences['budget'], car['Price_Min_Lakh'], car['Price_Max_Lakh']
            ),
            'fuel_type': calculate_match_score(
                user_preferences['fuel_type'], car['Fuel_Type_Full']
            ),
            'transmission': calculate_match_score(
                user_preferences['transmission'], car['Transmission_Full']
            ),
            'body_type': calculate_body_type_score(
                user_preferences['body_type'], car['Body_Type']
            ),
            'seating': calculate_seating_score(
                user_preferences['seating'], car['Seating_Min'], car['Seating_Max']
            ),
            'mileage': calculate_mileage_score(
                user_preferences['min_mileage'], car['Mileage_Avg_kmpl']
            ),
            'safety': calculate_safety_score(
                user_preferences['min_safety'], car['Safety_Rating']
            ),
        }

        final_score = sum(scores[key] * SCORE_WEIGHTS[key] for key in SCORE_WEIGHTS)
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

    results = pd.DataFrame(scored_cars).sort_values('Match_Percent', ascending=False)
    return results.head(number_of_results)


# Quick manual test - run this file directly to see sample output
if __name__ == '__main__':
    cars = load_car_data('datasets/raw/cars_in.csv')

    my_preferences = {
        'budget': 7,
        'fuel_type': 'Petrol',
        'transmission': 'Manual',
        'body_type': 'Hatchback',
        'seating': 5,
        'min_mileage': 18,
        'min_safety': 3,
    }

    top_matches = get_top_recommendations(my_preferences, cars)
    for _, row in top_matches.iterrows():
        print(f"{row['Brand']} {row['Model']} - {row['Match_Percent']}% match")
        print(f"  Reasons: {', '.join(row['Match_Reasons'])}")
        print()