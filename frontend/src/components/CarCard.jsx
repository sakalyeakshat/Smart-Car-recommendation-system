import React from "react";

function CarCard({ car, featured, compareList, onToggleCompare, onExplore }) {
  const isSelected = compareList.some(
    (c) => c.brand === car.brand && c.model === car.model
  );

  return (
    <div className={featured ? "car-card featured-card" : "car-card"}>

      <div className="car-header">
        <div>
          <h2>{car.brand} {car.model}</h2>
          <p className="car-price">₹ {car.price_range_lakh} Lakh</p>
        </div>

        <div className="match-score">
          {car.match_percent}%
        </div>
      </div>

      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${car.match_percent}%` }}
        ></div>
      </div>

      <div className="car-details">
        <div className="detail-box">
          <span>🚗 Body</span>
          <strong>{car.body_type}</strong>
        </div>

        <div className="detail-box">
          <span>⛽ Fuel</span>
          <strong>{car.fuel_type}</strong>
        </div>

        <div className="detail-box">
          <span>⚙ Transmission</span>
          <strong>{car.transmission}</strong>
        </div>
      </div>

      {car.match_reasons && car.match_reasons.length > 0 && (
        <div className="reason-section">
          <ul>
            {car.match_reasons.map((reason, index) => (
              <li key={index}> {reason}</li>
            ))}
          </ul>
        </div>
      )}

      <label className="compare-checkbox">
        <input
          type="checkbox"
          checked={isSelected}
          onChange={() => onToggleCompare(car)}
        />
        Compare
      </label>

      <button className="explore-button" onClick={() => onExplore(car)}>
        Explore More
      </button>

    </div>
  );
}

export default CarCard;