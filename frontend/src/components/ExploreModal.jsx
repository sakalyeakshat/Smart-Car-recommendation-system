import "../styles/ExploreModal.css";

function getKeyStrengths(car) {
  const strengths = [];

  if (car.body_type === "SUV") {
    strengths.push("Spacious cabin with better road presence.");
    strengths.push("Higher ground clearance handles rough roads with ease.");
  }

  if (car.body_type === "Sedan") {
    strengths.push("Balanced handling with a lower center of gravity.");
    strengths.push("Larger boot space, ideal for family trips.");
  }

  if (car.body_type === "Hatchback") {
    strengths.push("Easy to maneuver and park in tight city spaces.");
  }

  if (car.transmission === "Automatic") {
    strengths.push("Comfortable to drive in city traffic.");
  }

  if (car.transmission === "Manual") {
    strengths.push("More control over performance and better fuel efficiency.");
  }

  if (car.fuel_type === "Electric") {
    strengths.push("Zero tailpipe emissions and low running cost.");
    strengths.push("Near-silent cabin with instant acceleration.");
  }

  if (car.fuel_type === "CNG") {
    strengths.push("Economical fuel option for daily commuting.");
  }

  if (car.fuel_type === "Diesel") {
    strengths.push("Suitable for long-distance driving.");
    strengths.push("Better torque for highway overtakes.");
  }

  if (car.fuel_type === "Petrol") {
    strengths.push("Smooth and refined driving experience.");
  }

  strengths.push("Backed by strong resale value in the used car market.");

  return strengths;
}

function getThingsToConsider(car) {
  const considerations = [];

  if (car.body_type === "SUV") {
    considerations.push("Requires slightly more parking space.");
  }

  if (car.body_type === "Sedan") {
    considerations.push("Lower ground clearance may be an issue on rough roads.");
  }

  if (car.transmission === "Manual") {
    considerations.push(
      "Manual transmission may require more effort in heavy traffic."
    );
  }

  if (car.fuel_type === "Diesel") {
    considerations.push("Diesel vehicles may have higher maintenance costs.");
  }

  if (car.fuel_type === "Electric") {
    considerations.push("Charging infrastructure should be considered.");
  }

  if (car.fuel_type === "Petrol") {
    considerations.push("Running costs can add up on long highway drives.");
  }

  if (car.fuel_type === "CNG") {
    considerations.push("Boot space is reduced due to the CNG cylinder.");
  }

  return considerations;
}

function ExploreModal({ car, onClose }) {
  if (!car) {
    return null;
  }

  const keyStrengths = getKeyStrengths(car);

  const thingsToConsider = getThingsToConsider(car);

  function handleSearchReviews() {
    const searchQuery = `${car.brand} ${car.model} review India`;

    window.open(
      `https://www.google.com/search?q=${encodeURIComponent(searchQuery)}`,
      "_blank"
    );
  }

  return (
    <div className="modal-overlay">
      <div className="explore-modal">

        <button
          className="modal-close"
          onClick={onClose}
        >
          ×
        </button>

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

        <button
          className="review-button"
          onClick={handleSearchReviews}
        >
        Search Reviews
        </button>

      </div>
    </div>
  );
}

export default ExploreModal;
