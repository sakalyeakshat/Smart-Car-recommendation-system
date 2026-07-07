import "../styles/ResultPage.css";

function ResultsPage({
  bestCar,
  remainingCars,
  loading,
  searched,
  error,
  recommendations,
  openExploreModal,
  setCurrentView,
}) {
  return (
    <div className="results-page">

      <div className="results-header">
        <button
          className="change-preference-btn"
          onClick={() => {
            setCurrentView("home");
            setTimeout(() => {
              document
                .getElementById("recommendation-form")
                ?.scrollIntoView({ behavior: "smooth", block: "start" });
            }, 100);
          }}
        >
          Change Preferences
        </button>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading-state">
          <div className="loader"></div>
          <h2>Finding the best cars for you...</h2>
          <p>Hang tight, matching vehicles to your criteria...</p>
        </div>
      )}

      {searched && !loading && recommendations.length === 0 && !error && (
        <div className="empty-state">
          <h2>No Cars Found</h2>
          <p>Try increasing your budget or relaxing some filters.</p>
        </div>
      )}

      {bestCar && (
        <div className="best-section">
          <h2>Top Recommendation</h2>
          <CarCard
            car={bestCar}
            featured={true}
            onExplore={openExploreModal}
          />
        </div>
      )}

      {remainingCars.length > 0 && (
        <div className="others-section">
          <h3>More Vehicles You May Like</h3>
          <div className="cars-grid">
            {remainingCars.map((car, index) => (
              <CarCard
                key={index}
                car={car}
                featured={false}
                onExplore={openExploreModal}
              />
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
function CarCard({ car, featured, onExplore }) {
  return (
    <div className={featured ? "car-card featured-card" : "car-card"}>

      <div className="match-score">
        {car.match_percent}%
      </div>

      <div className="car-header">
        <h2>{car.brand} {car.model}</h2>
        <p className="car-price">₹ {car.price_range_lakh} Lakh</p>
      </div>

      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${car.match_percent}%` }}
        ></div>
      </div>

      <div className="car-details">
        <div className="detail-box">
          <span>Body</span>
          <strong>{car.body_type}</strong>
        </div>

        <div className="detail-box">
          <span>Fuel</span>
          <strong>{car.fuel_type}</strong>
        </div>

        <div className="detail-box">
          <span>Transmission</span>
          <strong>{car.transmission}</strong>
        </div>
      </div>

      {car.match_reasons && car.match_reasons.length > 0 && (
        <div className="reason-section">
          <ul>
            {car.match_reasons.map((reason, index) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>
        </div>
      )}

      <button className="explore-button" onClick={() => onExplore(car)}>
        Explore More
      </button>

    </div>
  );
}



export default ResultsPage;