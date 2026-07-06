import "../styles/CompareModal.css";
function CompareModal({ cars, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="compare-modal-content" onClick={(e) => e.stopPropagation()}>

        <button type="button" className="modal-close" onClick={onClose}>×</button>

        <h2>Comparing Your Picks</h2>

        <div className="compare-table">
          <div className="compare-row compare-header-row">
            <div className="compare-label"></div>
            {cars.map((car, i) => (
              <div key={i} className="compare-col-title">{car.brand} {car.model}</div>
            ))}
          </div>

          <div className="compare-row">
            <div className="compare-label">Match</div>
            {cars.map((car, i) => (<div key={i}>{car.match_percent}%</div>))}
          </div>

          <div className="compare-row">
            <div className="compare-label">Price Range</div>
            {cars.map((car, i) => (<div key={i}>₹ {car.price_range_lakh} Lakh</div>))}
          </div>

          <div className="compare-row">
            <div className="compare-label">Body Type</div>
            {cars.map((car, i) => (<div key={i}>{car.body_type}</div>))}
          </div>

          <div className="compare-row">
            <div className="compare-label">Fuel Type</div>
            {cars.map((car, i) => (<div key={i}>{car.fuel_type}</div>))}
          </div>

          <div className="compare-row">
            <div className="compare-label">Transmission</div>
            {cars.map((car, i) => (<div key={i}>{car.transmission}</div>))}
          </div>

          <div className="compare-row">
            <div className="compare-label">Safety Rating</div>
            {cars.map((car, i) => (<div key={i}>{car.safety_rating} Stars</div>))}
          </div>
        </div>

      </div>
    </div>
  );
}

export default CompareModal;