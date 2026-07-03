from pathlib import Path

from app.recommendation.recommend import (
    load_car_data,
    get_top_recommendations,
)


class RecommendationService:

    def __init__(self):

        # Docker-safe path (IMPORTANT FIX)
        BASE_DIR = Path("/app")

        dataset_path = BASE_DIR / "datasets" / "raw" / "cars_in.csv"

        self.cars_df = load_car_data(dataset_path)

    def recommend_cars(self, user_input):

        recommendations = get_top_recommendations(
            user_preferences=user_input,
            car_dataframe=self.cars_df,
            number_of_results=5,
        )

        # Rename columns for API response
        recommendations = recommendations.rename(
            columns={
                "Brand": "brand",
                "Model": "model",
                "Body_Type": "body_type",
                "Price_Range_Lakh": "price_range_lakh",
                "Fuel_Type": "fuel_type",
                "Transmission": "transmission",
                "Safety_Rating": "safety_rating",
                "Match_Percent": "match_percent",
                "Match_Reasons": "match_reasons",
            }
        )

        return recommendations.to_dict(orient="records")