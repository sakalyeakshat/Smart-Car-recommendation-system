# Smart Car Recommendation System — API Documentation

The backend service is built using **FastAPI** (Python) and runs inside a containerized Docker container.

## Base URL
```text
http://localhost:8089
```

## Interactive API Documentation
FastAPI automatically generates interactive visual documentation for the API:
* **Swagger UI**: [http://localhost:8089/docs](http://localhost:8089/docs) (Interactive testing & documentation)

---

## Endpoint Directory

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/` | Root verification status check. |
| **GET** | `/health` | Container and database connection health check. |
| **POST** | `/recommend` | Generates a list of vehicle recommendations based on user preferences. |

---

## 1. Verify Status Check
### Request
`GET /`

### Response (200 OK)
```json
{
  "message": "Backend is running!"
}
```

---

## 2. Health Check
### Request
`GET /health`

### Response (200 OK)
```json
{
  "status": "OK",
  "healthy": true
}
```

---

## 3. Generate Car Recommendations
### Request
`POST /recommend`

### Request Body (JSON)
The payload requires the user's budget and vehicle preferences:

```json
{
  "budget": 12.5,
  "fuel_type": "Petrol",
  "transmission": "Manual",
  "body_type": "SUV",
  "seating": 5,
  "min_mileage": 18.0,
  "min_safety": 4.0
}
```

### Request Parameter Specifications & Validation Rules
FastAPI enforces strict validation using **Pydantic** models. Requests containing invalid data types or out-of-range bounds are rejected with a `422 Unprocessable Entity` error.

| Field Name | Data Type | Validation Constraints | Description |
| :--- | :--- | :--- | :--- |
| `budget` | Float | Required, must be greater than 0 (`gt=0`) | User's car purchasing budget in Lakhs (e.g., `12.5` represents ₹12,50,000). |
| `fuel_type` | String | Required | Desired fuel type choice (e.g., `Petrol`, `Diesel`, `CNG`, `Electric`, `Hybrid`). |
| `transmission` | String | Required | Desired transmission choice (e.g., `Manual`, `Automatic`). |
| `body_type` | String | Required | Desired body design (e.g., `Hatchback`, `Sedan`, `SUV`, `MPV`, `Van`). |
| `seating` | Integer | Required, must be $\ge 2$ (`ge=2`) | Minimum passenger seating capacity requested. |
| `min_mileage` | Float | Required, range $[0.0, 30.0]$ (`ge=0, le=30`) | Minimum acceptable mileage in kmpl. |
| `min_safety` | Float | Required, range $[0.0, 5.0]$ (`ge=0, le=5`) | Minimum acceptable Global NCAP crash safety rating stars. |

---

### Response (200 OK)
Returns a JSON object with a list of up to 5 recommended cars matching the criteria, sorted by match percentage.

```json
{
  "recommendations": [
    {
      "brand": "Tata",
      "model": "Nexon",
      "body_type": "SUV",
      "price_range_lakh": "8.1 - 15.5",
      "fuel_type": "Petrol & Diesel",
      "transmission": "Manual & Automatic",
      "safety_rating": 5.0,
      "match_percent": 96.5,
      "match_reasons": [
        "Fits Your Budget",
        "Fuel: Petrol",
        "Transmission: Manual",
        "SUV Body Style",
        "5 Seater Comfort",
        "5 Star Safety Rated",
        "Good Mileage"
      ],
      "engine_cc": "1199 CC - 1497 CC",
      "exact_mileage": "17.01 kmpl to 24.08 kmpl",
      "safety_details": "5 Stars (Global NCAP)",
      "seating_capacity": "5 Seater",
      "ground_clearance": "210mm",
      "boot_space": "400L",
      "drive_type": "FWD",
      "fuel_tank_capacity": "50L"
    },
    {
      "brand": "Maruti",
      "model": "Brezza",
      "body_type": "SUV",
      "price_range_lakh": "8.34 - 14.14",
      "fuel_type": "Petrol & CNG",
      "transmission": "Manual & Automatic",
      "safety_rating": 5.0,
      "match_percent": 94.0,
      "match_reasons": [
        "Fits Your Budget",
        "Fuel: Petrol",
        "Transmission: Manual",
        "SUV Body Style",
        "5 Seater Comfort",
        "5 Star Safety Rated",
        "Good Mileage"
      ],
      "engine_cc": "1462 CC",
      "exact_mileage": "19.05 kmpl to 25.51 kmpl",
      "safety_details": "5 Stars",
      "seating_capacity": "5 Seater",
      "ground_clearance": "210mm",
      "boot_space": "400L",
      "drive_type": "FWD",
      "fuel_tank_capacity": "50L"
    }
  ]
}
```

---

## Error Handling & Response Validation

The API handles incorrect or malformed requests gracefully.

### Validation Errors (422 Unprocessable Entity)
If required fields are missing, contain incorrect data types, or violate range bounds (e.g. `min_safety: 6.0` or `budget: -5.0`), the server returns a details object outlining the failure:

```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["body", "min_safety"],
      "msg": "Input should be less than or equal to 5",
      "input": 6.0,
      "ctx": {
        "le": 5.0
      }
    }
  ]
}
```
