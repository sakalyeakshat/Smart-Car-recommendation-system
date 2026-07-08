# Usage Guide

This guide explains how to use the Smart Car Recommendation System UI to find personalized vehicle recommendations tailored to your exact profile.

## How to use the App

Open the Application: Make sure the Docker containers are running, then navigate to http://localhost:3000 in your web browser.

Select your Parameters: Use the form fields to define your specific constraints:
* Budget (in Lakhs): Enter your maximum budget.
* Fuel Type Preference: Choose Petrol, Diesel, CNG, or Electric.
* Transmission Preference: Select Manual or Automatic.
* Seating Capacity: Pick the number of seats you need.
* Minimum Safety Rating: Select the required NCAP safety stars.
* Body Type: Choose Hatchback, Sedan, SUV, or MUV.
* Minimum Mileage: Input your desired fuel efficiency (kmpl).

Submit: Click the "Find Best Matches" button to query the matching engine.

## Reading the Results

The system will return the top 5 best-fitting vehicles based on the weighted scoring algorithm.

* Match Percentage: This is a mathematical score out of 100%. It is calculated based on how closely the car fits your exact requirements, with partial credit awarded for secondary matches or close approximations.
* Match Reasons: This explicitly lists exactly why this car was recommended to you, highlighting the parameters that perfectly aligned with your input.
* Explore More: Clicking this button on any recommendation card opens a detailed modal showing the specific strengths and trade-offs of that vehicle compared to your original preferences.

## Worked Example

Let's assume you submit the following profile:
* Budget: 12.0 Lakhs
* Fuel: Petrol
* Transmission: Automatic
* Body Type: SUV

Expected Output: The algorithm will likely return a vehicle like the Hyundai Creta as a top match.

* You receive high points because the car fits perfectly within the 12.0 Lakh budget constraint.
* The UI will list "Fuel: Petrol" and "SUV Body Style" under the Match Reasons, informing you exactly why this specific model is a great fit for your daily needs.
