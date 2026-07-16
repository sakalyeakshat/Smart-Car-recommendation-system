"""Core recommendation engine with TF-IDF similarity and scoring functions."""

import pandas as pd
import math
import re
from config import SCORE_WEIGHTS

THRESHOLD = 0.7
MILEAGE_PLACEHOLDER = 19.6

class SimpleTFIDF:
    """TF-IDF vectorizer and cosine similarity calculator for text features."""

    def __init__(self, corpus):
        """Build IDF vocabulary and counts from input document corpus."""
        self.idf = {}
        self.vocabulary = set()
        self.doc_count = len(corpus)
        
        counts = {}
        for doc in corpus:
            tokens = self._tokenize(doc)
            for t in set(tokens):
                counts[t] = counts.get(t, 0) + 1
                
        for term, df in counts.items():
            self.idf[term] = math.log((1 + self.doc_count) / (1 + df)) + 1
            self.vocabulary.add(term)

    def _tokenize(self, text):
        """Tokenize input text using regex matching alphanumeric characters."""
        if not isinstance(text, str):
            return []
        return re.findall(r'\w+', text.lower())

    def get_vector(self, text):
        """Convert input text to a dictionary-based TF-IDF sparse vector."""
        tokens = self._tokenize(text)
        tf = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
            
        vec = {}
        for term, count in tf.items():
            if term in self.vocabulary:
                vec[term] = count * self.idf[term]
        return vec

    def calculate_similarity(self, text_a, text_b):
        """Compute the Cosine Similarity between two text specifications."""
        if not text_a or not text_b:
            return 0.0
        vec_a = self.get_vector(str(text_a))
        vec_b = self.get_vector(str(text_b))
        
        dot = 0.0
        for term in vec_a:
            if term in vec_b:
                dot += vec_a[term] * vec_b[term]
                
        n_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
        n_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
        
        if n_a == 0.0 or n_b == 0.0:
            return 0.0
            
        return dot / (n_a * n_b)

def get_budget_score(budget, min_p, max_p):
    """Calculate the budget proximity score from 0.0 to 1.0."""
    if pd.isna(min_p) or pd.isna(max_p):
        return 0
    if min_p <= budget <= max_p:
        return 1.0
    gap = min(abs(budget - min_p), abs(budget - max_p))
    penalty = gap / max(budget, 1)
    return max(0, 1 - penalty)

def check_user_prefs(pref_list, full_spec, tfidf):
    """Compare user specs preference against vehicle specs using TF-IDF."""
    if pd.isna(full_spec) or not pref_list:
        return 0.0
    q = " ".join(pref_list)
    return tfidf.calculate_similarity(q, full_spec)

def get_body_score(u_body, c_body, tfidf):
    """Calculate similarity between preferred body and actual car body style."""
    if pd.isna(c_body) or pd.isna(u_body):
        return 0.0
    return tfidf.calculate_similarity(u_body, c_body)

def get_mileage_score(min_mil, avg_mil):
    """Compare car fuel economy against user requested minimum mileage."""
    if pd.isna(avg_mil):
        return 0.5
    if abs(avg_mil - MILEAGE_PLACEHOLDER) < 0.01:
        return 0.5
    if min_mil == 0:
        return 1.0
    if avg_mil >= min_mil:
        return 1.0
    return max(0, avg_mil / max(min_mil, 1))

def get_range_score(min_range, c_range):
    """Calculate EV battery driving range score against user requirements."""
    if pd.isna(c_range) or c_range == 0:
        return 0.5
    if min_range == 0:
        return 1.0
    if c_range >= min_range:
        return 1.0
    return max(0, c_range / max(min_range, 1))

def get_seating_score(u_seats, min_s, max_s):
    """Assess compatibility of seating capacity with user preferences."""
    if pd.isna(min_s) or pd.isna(max_s):
        return 0
    if min_s <= u_seats <= max_s:
        return 1.0
    if max_s < u_seats:
        return 0.0
    return 0.75

def get_safety_score(u_safety, c_safety):
    """Calculate score for vehicle crash safety rating compatibility."""
    if pd.isna(c_safety):
        return 0.5
    if c_safety >= u_safety:
        return 1.0
    return max(0, c_safety / max(u_safety, 1))

def make_reasons_list(prefs, car, scores):
    """Assemble descriptive badge names for scores meeting match threshold."""
    reasons = []
    if scores['budget'] >= THRESHOLD:
        reasons.append("Fits Your Budget")
    if scores['fuel_type'] >= THRESHOLD:
        reasons.append(f"Fuel: {', '.join(prefs['fuel_type'])}")
    if scores['transmission'] >= THRESHOLD:
        reasons.append(f"Transmission: {', '.join(prefs['transmission'])}")
    if scores['body_type'] >= THRESHOLD:
        reasons.append(f"{car['Body_Type']} Body Style")
    if scores['seating'] >= THRESHOLD:
        reasons.append(f"{prefs['seating']} Seater Comfort")
    if scores['safety'] >= THRESHOLD:
        reasons.append(f"{car['Safety_Rating']} Star Safety Rated")
    if scores['mileage'] >= THRESHOLD:
        is_ev = str(car.get('Fuel_Type_Primary', '')).strip().lower() == 'electric'
        if is_ev:
            reasons.append("Good Driving Range")
        else:
            reasons.append("Good Mileage")
    return reasons

def mix_brands(df, top_n):
    """Enforce brand diversity constraint by selecting unique manufacturer names first."""
    seen = set()
    primary = []
    overflow = []
    for _, row in df.iterrows():
        b = row['brand']
        if b not in seen:
            seen.add(b)
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
    """Execute pre-filtering and weighted similarity calculations to return ranked matches."""
    cars = df.copy()
    ceiling = prefs['budget'] * 1.3
    u_seats = prefs['seating']
    u_range = prefs.get('min_range', 0) or 0
    
    # filter out cars exceeding budget or seating
    filtered = cars[
        (cars['Price_Min_Lakh'] <= ceiling) &
        (cars['Seating_Max'] >= u_seats)
    ]
    
    if filtered.empty:
        return pd.DataFrame(columns=[
            "brand", "model", "body_type", "price_range_lakh",
            "fuel_type", "transmission", "safety_rating",
            "match_percent", "match_reasons"
        ])
        
    corpus = []
    for _, row in df.iterrows():
        fuel = str(row.get('Fuel_Type_Full', ''))
        trans = str(row.get('Transmission_Full', ''))
        body = str(row.get('Body_Type', ''))
        corpus.append(f"{fuel} {trans} {body}")
        
    tfidf = SimpleTFIDF(corpus)
    results = []
    
    for _, car in filtered.iterrows():
        is_ev = str(car.get('Fuel_Type_Primary', '')).strip().lower() == 'electric'
        
        if is_ev:
            mil_score = get_range_score(u_range, car.get('Range_km', 0))
        else:
            mil_score = get_mileage_score(prefs['min_mileage'], car['Mileage_Avg_kmpl'])
 
        scores = {
            'budget': get_budget_score(prefs['budget'], car['Price_Min_Lakh'], car['Price_Max_Lakh']),
            'fuel_type': check_user_prefs(prefs['fuel_type'], car['Fuel_Type_Full'], tfidf),
            'transmission': check_user_prefs(prefs['transmission'], car['Transmission_Full'], tfidf),
            'body_type': get_body_score(prefs['body_type'], car['Body_Type'], tfidf),
            'seating': get_seating_score(prefs['seating'], car['Seating_Min'], car['Seating_Max']),
            'mileage': mil_score,
            'safety': get_safety_score(prefs['min_safety'], car['Safety_Rating']),
        }
        
        if scores['fuel_type'] == 0.0 or scores['transmission'] == 0.0 or scores['body_type'] == 0.0:
            continue
        
        tot = sum(scores[k] * SCORE_WEIGHTS[k] for k in SCORE_WEIGHTS)
        
        eng_min = car.get('Engine_Min_CC', 0)
        eng_max = car.get('Engine_Max_CC', 0)
        eng_cc = "N/A"
        if is_ev:
            eng_cc = "N/A (EV)"
        elif not pd.isna(eng_min):
            if eng_min == eng_max or pd.isna(eng_max):
                eng_cc = f"{int(eng_min)} CC"
            else:
                eng_cc = f"{int(eng_min)} CC - {int(eng_max)} CC"
        
        exact_mil = "N/A"
        if is_ev:
            r_val = car.get('Range_km')
            exact_mil = f"{int(r_val)} km" if pd.notna(r_val) else "N/A (EV)"
        else:
            mil_min = car.get('Mileage_Min_kmpl', 0)
            mil_max = car.get('Mileage_Max_kmpl', 0)
            if not pd.isna(mil_min):
                if mil_min == mil_max or pd.isna(mil_max):
                    exact_mil = f"{mil_min} kmpl"
                else:
                    exact_mil = f"{mil_min} kmpl to {mil_max} kmpl"
        
        saf_val = car.get('Safety_Rating', 0)
        ncap = car.get('NCAP_Body', '')
        if pd.isna(saf_val):
            saf_details = "Not Tested"
        else:
            saf_details = f"{int(saf_val)} Stars"
            if pd.notna(ncap) and ncap != "":
                saf_details += f" ({ncap})"
        
        s_max = car.get('Seating_Max', 0)
        seat_cap = "N/A"
        if not pd.isna(s_max):
            seat_cap = f"{int(s_max)} Seater"
  
        results.append({
            "brand": car["Brand"],
            "model": car["Model"],
            "body_type": car["Body_Type"],
            "price_range_lakh": f"{car['Price_Min_Lakh']} - {car['Price_Max_Lakh']}",
            "fuel_type": car["Fuel_Type_Full"],
            "transmission": car["Transmission_Full"],
            "safety_rating": 0.0 if pd.isna(car["Safety_Rating"]) else float(car["Safety_Rating"]),
            "match_percent": round(tot * 100, 1),
            "match_reasons": make_reasons_list(prefs, car, scores),
            "engine_cc": eng_cc,
            "exact_mileage": exact_mil,
            "safety_details": saf_details,
            "seating_capacity": seat_cap,
            "ground_clearance": "N/A" if pd.isna(car.get("Ground_Clearance_mm")) else str(car.get("Ground_Clearance_mm")),
            "boot_space": "N/A" if pd.isna(car.get("Boot_Space_Liters")) else str(car.get("Boot_Space_Liters")),
            "drive_type": "N/A" if pd.isna(car.get("Drive_Type")) else str(car.get("Drive_Type")),
            "fuel_tank_capacity": "N/A" if pd.isna(car.get("Fuel_Tank_Capacity_Liters")) else str(car.get("Fuel_Tank_Capacity_Liters")),
        })
        
    if not results:
        return pd.DataFrame(columns=[
            "brand", "model", "body_type", "price_range_lakh",
            "fuel_type", "transmission", "safety_rating",
            "match_percent", "match_reasons", "engine_cc",
            "exact_mileage", "safety_details", "seating_capacity",
            "ground_clearance", "boot_space", "drive_type", "fuel_tank_capacity"
        ])
 
    ranked = pd.DataFrame(results).sort_values(by="match_percent", ascending=False).reset_index(drop=True)
    return mix_brands(ranked, top_n)
