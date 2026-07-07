import "../styles/ExploreModal.css";

function ExploreModal({ car, onClose }) {
  if (!car) return null;

  return (
    <div className="modal-overlay">
      <div className="explore-modal">
        <button className="modal-close" onClick={onClose}>×</button>

        <div className="explore-header">
          <h2>{car.brand} {car.model}</h2>
        </div>

        <div className="specs-grid">
          {[
            { label: "Engine Capacity", value: car.engine_cc },
            { label: "Exact Mileage", value: car.exact_mileage },
            { label: "Safety Details", value: car.safety_details },
            { label: "Seating Capacity", value: car.seating_capacity },
            { label: "Ground Clearance", value: car.ground_clearance },
            { label: "Boot Space", value: car.boot_space },
            { label: "Drive Type", value: car.drive_type },
            { label: "Fuel Tank Capacity", value: car.fuel_tank_capacity }
          ].map((spec, index) => (
            <div key={index} className="spec-item">
              <span className="spec-label">{spec.label}</span>
              <span className="spec-value">{spec.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ExploreModal;
