


CREATE DATABASE IF NOT EXISTS smart_car_recommendation_system;
USE smart_car_recommendation_system;

CREATE TABLE IF NOT EXISTS cars (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    Brand                   VARCHAR(100),
    Model                   VARCHAR(150),
    Body_Type               VARCHAR(50),
    Price_Min_Lakh          FLOAT,
    Price_Max_Lakh          FLOAT,
    Price_Avg_Lakh          FLOAT,
    Price_INR               BIGINT,
    Mileage_Min_kmpl        FLOAT,
    Mileage_Max_kmpl        FLOAT,
    Mileage_Avg_kmpl        FLOAT,
    Engine_Min_CC           FLOAT,
    Engine_Max_CC           FLOAT,
    Engine_Avg_CC           FLOAT,
    Safety_Rating           FLOAT,
    Safety_Rating_Available VARCHAR(10),
    NCAP_Body               VARCHAR(100),
    Fuel_Type_Primary       VARCHAR(50),
    Fuel_Type_Full          VARCHAR(100),
    Transmission_Primary    VARCHAR(50),
    Transmission_Full       VARCHAR(100),
    Seating_Min             INT,
    Seating_Max             INT
);
