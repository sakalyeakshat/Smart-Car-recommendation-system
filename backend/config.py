"""
Configuration settings for the Smart Car Recommendation System backend.
Contains weight definitions for the scoring algorithm and other constants.
"""

"""
Weights for each preference used in the scoring algorithm.
Budget is the most important factor, mileage and seating the least.
"""
SCORE_WEIGHTS = {
    'budget':       0.30,
    'fuel_type':    0.20,
    'transmission': 0.15,
    'safety':       0.15,
    'body_type':    0.10,
    'seating':      0.05,
    'mileage':      0.05,
}

TOP_N_RECOMMENDATIONS = 5
