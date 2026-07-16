/**
 * @file ExploreModal.jsx
 * @description Modal dialog component that displays detailed technical specifications
 * for a selected car. It shows specs such as engine capacity (or motor/battery for
 * electric vehicles), mileage/range, safety details, seating capacity, ground
 * clearance, boot space, drive type, and fuel tank capacity in a grid layout.
 * The modal is triggered from the ResultsPage when the user clicks "Explore More".
 */
import "../styles/ExploreModal.css";

/**
 * Overlay modal that presents the full specification sheet for a given car.
 */
function ExploreModal({ car, onClose }) {
  if (!car) return null;

  const isElectric = car.fuel_type && car.fuel_type.toLowerCase().includes("electric");

  return (
    <div className="modal-overlay">
      <div className="explore-modal">
        <button className="modal-close" onClick={onClose}>×</button>

        <div className="explore-header">
          <h2>{car.brand} {car.model}</h2>
        </div>

        <div className="specs-grid">
          {[
            { label: isElectric ? "Motor / Battery" : "Engine Capacity", value: car.engine_cc },
            { label: isElectric ? "Driving Range" : "Exact Mileage", value: car.exact_mileage },
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
