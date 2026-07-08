# Data Preparation

This project uses the Indian Cars under 20 Lakhs dataset from Kaggle, containing detailed records of cars under 20 Lakhs, enriched with specs like Brand, Model, Price, Mileage, Safety Ratings, Seating, Fuel, and Transmission.

## Why Preprocessing Was Necessary
The recommendation engine relies on clean, numeric, and normalized values in the price, mileage, and safety rating fields to build a mathematical similarity score and rank results accurately. Without handling missing values, CC range formats, and manually enriching empty columns, the matching logic would either crash outright or silently produce misleading recommendations.

## Preprocessing Steps
All of this happens inside `backend/recommender/services.py` during database initialization before the data is queried.

**Missing Text & Numeric Fields**
Missing values for safety ratings, seatings, or mileage are normalized to standard defaults to avoid database query syntax errors. Default values ensure the engine can run mathematical comparisons consistently without encountering null pointer issues.

**The CC Range & Casing Problem**
The raw dataset contains engine sizes as strings with ranges (like "1199 CC - 1497 CC") or literal CC labels. A plain numeric conversion on these values throws ValueError. We normalized engine capacity fields into consistent CC sizes to allow formatting and range filtering. Additionally, transmission and fuel types were normalized in casing so they query successfully against user preferences.

**Why Specifications are Enriched and Stored as Text**
Critical parameters like ground clearance (e.g., "170mm"), boot space (e.g., "300L"), and drive type (e.g., "FWD") are manually researched, added, and stored as text fields. Since these features are displayed inside the "Explore More" details modal rather than used as hard scoring attributes, keeping them as formatted strings simplifies representation and sidesteps numeric type conversion issues.

## Inserting Into MySQL
After cleaning and preprocessing, the dataset is imported into the MySQL database using SQLAlchemy and Pandas' `to_sql` method, which dynamically maps the DataFrame to a relational table structure.

Before importing, the seeding script queries the MySQL database to check if the `cars` table already contains rows, and exits immediately if it does. This makes it safe for the seeding function to run every time the backend container starts without ever creating duplicate rows on a restart.

## Dataset Source
Dataset used, Indian Cars under 20 Lakhs.

Source, https://www.kaggle.com/datasets/shiivvvaam/indian-cars-under-20-lakhs
