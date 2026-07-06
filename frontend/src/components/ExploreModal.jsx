import "../styles/ExploreModal.css";

// Helper — case-insensitive substring check
const has = (str, keyword) =>
  str ? str.toLowerCase().includes(keyword.toLowerCase()) : false;

function getKeyStrengths(car) {
  const strengths = [];
  const fuel = car.fuel_type || "";
  const tx   = car.transmission || "";
  const body = car.body_type || "";

  // ── Body type ── (one point each to keep the list concise)
  if (has(body, "SUV")) {
    strengths.push("Spacious cabin with better road presence and higher ground clearance.");
  }
  if (has(body, "Sedan")) {
    strengths.push("Balanced handling with a lower center of gravity and large boot space.");
  }
  if (has(body, "Hatchback")) {
    strengths.push("Easy to manoeuvre and park in tight city spaces.");
  }
  if (has(body, "MPV")) {
    strengths.push("Generous seating capacity with a flexible cabin layout.");
  }
  if (has(body, "Van")) {
    strengths.push("Maximum passenger or cargo capacity for large groups.");
  }
  if (has(body, "Pickup")) {
    strengths.push("High payload capacity with a rugged build for off-road use.");
  }

  // ── Transmission ──
  if (has(tx, "Automatic")) {
    strengths.push("Comfortable to drive in city traffic — no clutch fatigue.");
  }
  if (has(tx, "Manual") && !has(tx, "Automatic")) {
    strengths.push("More driver control with better fuel efficiency.");
  }

  // ── Fuel type ──
  if (has(fuel, "Electric")) {
    strengths.push("Zero tailpipe emissions and very low running cost.");
    strengths.push("Near-silent cabin with instant torque from standstill.");
  }
  if (has(fuel, "Hybrid")) {
    strengths.push("Best-of-both-worlds efficiency — petrol + electric.");
    strengths.push("Regenerative braking helps top up the battery automatically.");
  }
  if (has(fuel, "CNG")) {
    strengths.push("CNG is significantly cheaper per km than petrol or diesel.");
  }
  if (has(fuel, "Diesel") && !has(fuel, "Electric")) {
    strengths.push("Excellent fuel efficiency on long highway drives.");
    strengths.push("Strong torque makes overtaking effortless.");
  }
  if (has(fuel, "Petrol") && !has(fuel, "Electric") && !has(fuel, "Hybrid")) {
    strengths.push("Smooth and refined petrol engine for everyday driving.");
  }

  return strengths;
}

function getThingsToConsider(car) {
  const considerations = [];
  const fuel = car.fuel_type || "";
  const tx   = car.transmission || "";
  const body = car.body_type || "";

  // ── Body type ── (one point each to keep the list concise)
  if (has(body, "SUV")) {
    considerations.push("Larger footprint means tighter parking in city areas.");
  }
  if (has(body, "Sedan")) {
    considerations.push("Lower ground clearance may struggle on broken roads.");
  }
  if (has(body, "Hatchback")) {
    considerations.push("Smaller boot space compared to sedans and SUVs.");
  }
  if (has(body, "MPV")) {
    considerations.push("Boxy design can feel large to park in cramped urban spaces.");
  }
  if (has(body, "Van")) {
    considerations.push("Driving a large van in city traffic requires experience.");
  }
  if (has(body, "Pickup")) {
    considerations.push("Open cargo bed provides no weather protection for goods.");
  }

  // ── Transmission ──
  if (has(tx, "Manual") && !has(tx, "Automatic")) {
    considerations.push("Constant clutch use can be tiring in heavy stop-go traffic.");
  }
  if (has(tx, "Automatic") && !has(tx, "Manual")) {
    considerations.push("Automatic gearbox can add to the service cost over time.");
  }

  // ── Fuel type ──
  if (has(fuel, "Diesel") && !has(fuel, "Electric")) {
    considerations.push("Diesel service intervals and repairs can be costlier.");
  }
  if (has(fuel, "Electric")) {
    considerations.push("Public charging infrastructure is still growing in India.");
    considerations.push("Long trips require planning around charging stops.");
  }
  if (has(fuel, "Hybrid")) {
    considerations.push("Hybrid battery replacement can be expensive in the long run.");
  }
  if (has(fuel, "Petrol") && !has(fuel, "Electric") && !has(fuel, "Hybrid")) {
    considerations.push("Running costs add up faster on long daily highway commutes.");
  }
  if (has(fuel, "CNG")) {
    considerations.push("CNG cylinder occupies boot space, reducing luggage room.");
    considerations.push("CNG filling stations are fewer outside major cities.");
  }

  // Fallback — guarantee at least one item always shows
  if (considerations.length === 0) {
    considerations.push("Evaluate your city's road and fuel infrastructure before purchasing.");
  }

  return considerations;
}


function ExploreModal({ car, onClose }) {
  if (!car) return null;

  const keyStrengths     = getKeyStrengths(car);
  const thingsToConsider = getThingsToConsider(car);

  return (
    <div className="modal-overlay">
      <div className="explore-modal">

        <button className="modal-close" onClick={onClose}>×</button>

        <h2>Why This Car Stands Out</h2>

        <div className="explore-section">
          <h3>Key Strengths</h3>
          <ul>
            {keyStrengths.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="explore-section">
          <h3>Things to Consider</h3>
          <ul>
            {thingsToConsider.map((item, index) => (
              <li key={index}>⚠ {item}</li>
            ))}
          </ul>
        </div>

      </div>
    </div>
  );
}

export default ExploreModal;
