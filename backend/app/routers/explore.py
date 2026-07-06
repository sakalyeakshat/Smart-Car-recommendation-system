from fastapi import APIRouter

from app.schemas.explore import ExploreRequest, ExploreResponse

router = APIRouter()


def _has(text: str, keyword: str) -> bool:
    return keyword.lower() in text.lower() if text else False


def _get_key_strengths(fuel, transmission, body):
    strengths = []

    # body type
    if _has(body, "SUV"):
        strengths.append("Spacious cabin with better road presence and higher ground clearance.")
    if _has(body, "Sedan"):
        strengths.append("Balanced handling with a lower center of gravity and large boot space.")
    if _has(body, "Hatchback"):
        strengths.append("Easy to manoeuvre and park in tight city spaces.")
    if _has(body, "MPV"):
        strengths.append("Generous seating capacity with a flexible cabin layout.")
    if _has(body, "Van"):
        strengths.append("Maximum passenger or cargo capacity for large groups.")
    if _has(body, "Pickup"):
        strengths.append("High payload capacity with a rugged build for off-road use.")

    # transmission
    if _has(transmission, "Automatic"):
        strengths.append("Comfortable to drive in city traffic — no clutch fatigue.")
    if _has(transmission, "Manual") and not _has(transmission, "Automatic"):
        strengths.append("More driver control with better fuel efficiency.")

    # fuel type
    if _has(fuel, "Electric"):
        strengths.append("Zero tailpipe emissions and very low running cost.")
        strengths.append("Near-silent cabin with instant torque from standstill.")
    if _has(fuel, "Hybrid"):
        strengths.append("Best-of-both-worlds efficiency — petrol + electric.")
        strengths.append("Regenerative braking helps top up the battery automatically.")
    if _has(fuel, "CNG"):
        strengths.append("CNG is significantly cheaper per km than petrol or diesel.")
    if _has(fuel, "Diesel") and not _has(fuel, "Electric"):
        strengths.append("Excellent fuel efficiency on long highway drives.")
        strengths.append("Strong torque makes overtaking effortless.")
    if _has(fuel, "Petrol") and not _has(fuel, "Electric") and not _has(fuel, "Hybrid"):
        strengths.append("Smooth and refined petrol engine for everyday driving.")

    return strengths


def _get_things_to_consider(fuel, transmission, body):
    considerations = []

    # body type
    if _has(body, "SUV"):
        considerations.append("Larger footprint means tighter parking in city areas.")
    if _has(body, "Sedan"):
        considerations.append("Lower ground clearance may struggle on broken roads.")
    if _has(body, "Hatchback"):
        considerations.append("Smaller boot space compared to sedans and SUVs.")
    if _has(body, "MPV"):
        considerations.append("Boxy design can feel large to park in cramped urban spaces.")
    if _has(body, "Van"):
        considerations.append("Driving a large van in city traffic requires experience.")
    if _has(body, "Pickup"):
        considerations.append("Open cargo bed provides no weather protection for goods.")

    # transmission
    if _has(transmission, "Manual") and not _has(transmission, "Automatic"):
        considerations.append("Constant clutch use can be tiring in heavy stop-go traffic.")
    if _has(transmission, "Automatic") and not _has(transmission, "Manual"):
        considerations.append("Automatic gearbox can add to the service cost over time.")

    # fuel type
    if _has(fuel, "Diesel") and not _has(fuel, "Electric"):
        considerations.append("Diesel service intervals and repairs can be costlier.")
    if _has(fuel, "Electric"):
        considerations.append("Public charging infrastructure is still growing in India.")
        considerations.append("Long trips require planning around charging stops.")
    if _has(fuel, "Hybrid"):
        considerations.append("Hybrid battery replacement can be expensive in the long run.")
    if _has(fuel, "Petrol") and not _has(fuel, "Electric") and not _has(fuel, "Hybrid"):
        considerations.append("Running costs add up faster on long daily highway commutes.")
    if _has(fuel, "CNG"):
        considerations.append("CNG cylinder occupies boot space, reducing luggage room.")
        considerations.append("CNG filling stations are fewer outside major cities.")

    if not considerations:
        considerations.append("Evaluate your city's road and fuel infrastructure before purchasing.")

    return considerations


@router.post("/explore", response_model=ExploreResponse)
def explore_car(payload: ExploreRequest):
    return ExploreResponse(
        key_strengths=_get_key_strengths(
            payload.fuel_type, payload.transmission, payload.body_type
        ),
        things_to_consider=_get_things_to_consider(
            payload.fuel_type, payload.transmission, payload.body_type
        )
    )
