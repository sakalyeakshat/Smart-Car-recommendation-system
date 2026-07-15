"""
Recommendation matching engine.
Contains the core logic and helper scoring functions for vehicle suggestions.
"""
import pandas as pd
import math
import re
from config import SCORE_WEIGHTS

THRESHOLD = 0.7
MILEAGE_PLACEHOLDER = 19.6


class SimpleTFIDF:
    def __init__(self, corpus):
        """
        Initialize the TF-IDF model and fit it on the provided corpus (list of strings).
        """
        self.idf = {}
        self.vocabulary = set()
        self.doc_count = len(corpus)
        
        # Tokenize and build document frequencies
        df_count = {}
        for doc in corpus:
            tokens = self._tokenize(doc)
            unique_tokens = set(tokens)
            for token in unique_tokens:
                df_count[token] = df_count.get(token, 0) + 1
                
        # Calculate IDF for each token
        for term, df in df_count.items():
            # Standard smooth IDF formula
            self.idf[term] = math.log((1 + self.doc_count) / (1 + df)) + 1
            self.vocabulary.add(term)

    def _tokenize(self, text):
        if not isinstance(text, str):
            return []
        # Convert to lowercase and match alphanumeric words
        return re.findall(r'\w+', text.lower())

    def get_vector(self, text):
        tokens = self._tokenize(text)
        tf = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
            
        tfidf_vec = {}
        for term, count in tf.items():
            if term in self.vocabulary:
                tfidf_vec[term] = count * self.idf[term]
        return tfidf_vec

    def cosine_similarity(self, text_a, text_b):
        if not text_a or not text_b:
            return 0.0
        vec_a = self.get_vector(str(text_a))
        vec_b = self.get_vector(str(text_b))
        
        dot_product = 0.0
        for term in vec_a:
            if term in vec_b:
                dot_product += vec_a[term] * vec_b[term]
                
        norm_a = math.sqrt(sum(val ** 2 for val in vec_a.values()))
        norm_b = math.sqrt(sum(val ** 2 for val in vec_b.values()))
        
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
            
        return dot_product / (norm_a * norm_b)


def get_budget_score(user_budget, min_price, max_price):
    """
    Calculates a proximity score based on target budget vs car price limits.
    Returns 1.0 if budget is within range, otherwise computes a linear penalty gap.
    """
    if pd.isna(min_price) or pd.isna(max_price):
        return 0
    if min_price <= user_budget <= max_price:
        return 1.0
        
    gap = min(abs(user_budget - min_price), abs(user_budget - max_price))
    penalty = gap / max(user_budget, 1)
    
    return max(0, 1 - penalty)


def check_user_prefs(user_pref, car_pref_full, tfidf):
    """
    Checks categorical preferences like transmission or fuel type.
    Computes Cosine Similarity between user preferences and database fields using TF-IDF.
    """
    if pd.isna(car_pref_full) or pd.isna(user_pref):
        return 0.0
    return tfidf.cosine_similarity(user_pref, car_pref_full)


def get_body_score(user_body, car_body, tfidf):
    """
    Calculates a body type match score using TF-IDF Cosine Similarity.
    """
    if pd.isna(car_body) or pd.isna(user_body):
        return 0.0
    return tfidf.cosine_similarity(user_body, car_body)



def get_mileage_score(user_min_mileage, car_avg_mileage):
    """
    Calculates a compatibility score based on the user's minimum mileage request.
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
    Calculates a seating capacity compatibility score.
    """
    if pd.isna(min_seats) or pd.isna(max_seats):
        return 0
    if min_seats <= user_seats <= max_seats:
        return 1.0
    if max_seats < user_seats:
        return 0.0
    
    return 0.75


def get_safety_score(user_safety, car_safety):
    
    if pd.isna(car_safety):
        return 0.5
    if car_safety >= user_safety:
        return 1.0
    return max(0, car_safety / max(user_safety, 1))


def make_reasons_list(prefs, car, scores):
    """
    Constructs a list of descriptive explanation reasons for high-scoring properties (>= 0.7).
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
    Enforces brand diversity in recommendations.
    Ensures that the top N matches represent unique manufacturers.
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
    
    cars = df.copy()
    
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
        
    # Build text corpus for TF-IDF from all cars in the database to fit vocabulary and IDFs
    corpus = []
    for _, row in df.iterrows():
        fuel = str(row.get('Fuel_Type_Full', ''))
        trans = str(row.get('Transmission_Full', ''))
        body = str(row.get('Body_Type', ''))
        corpus.append(f"{fuel} {trans} {body}")
        
    tfidf = SimpleTFIDF(corpus)
        
    results = []
    for _, car in filtered_cars.iterrows():
        scores = {
            'budget': get_budget_score(prefs['budget'], car['Price_Min_Lakh'], car['Price_Max_Lakh']),
            'fuel_type': check_user_prefs(prefs['fuel_type'], car['Fuel_Type_Full'], tfidf),
            'transmission': check_user_prefs(prefs['transmission'], car['Transmission_Full'], tfidf),
            'body_type': get_body_score(prefs['body_type'], car['Body_Type'], tfidf),
            'seating': get_seating_score(prefs['seating'], car['Seating_Min'], car['Seating_Max']),
            'mileage': get_mileage_score(prefs['min_mileage'], car['Mileage_Avg_kmpl']),
            'safety': get_safety_score(prefs['min_safety'], car['Safety_Rating']),
        }
        
        total_score = 0
        for key in SCORE_WEIGHTS:
            total_score += scores[key] * SCORE_WEIGHTS[key]
        
        engine_min = car.get('Engine_Min_CC', 0)
        engine_max = car.get('Engine_Max_CC', 0)
        engine_cc = "N/A"
        if not pd.isna(engine_min):
            if engine_min == engine_max or pd.isna(engine_max):
                engine_cc = f"{int(engine_min)} CC"
            else:
                engine_cc = f"{int(engine_min)} CC - {int(engine_max)} CC"
        
        mil_min = car.get('Mileage_Min_kmpl', 0)
        mil_max = car.get('Mileage_Max_kmpl', 0)
        exact_mileage = "N/A"
        if not pd.isna(mil_min):
            if mil_min == mil_max or pd.isna(mil_max):
                exact_mileage = f"{mil_min} kmpl"
            else:
                exact_mileage = f"{mil_min} kmpl to {mil_max} kmpl"
        
        safety_rating_val = car.get('Safety_Rating', 0)
        ncap_body = car.get('NCAP_Body', '')
        
        if pd.isna(safety_rating_val):
            safety_details = "Not Tested"
        else:
            safety_details = f"{int(safety_rating_val)} Stars"
            if pd.notna(ncap_body) and ncap_body != "":
                safety_details += f" ({ncap_body})"
        
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
        
    ranked = pd.DataFrame(results).sort_values(by="match_percent", ascending=False).reset_index(drop=True)
    return mix_brands(ranked, top_n)
