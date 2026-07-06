import "../styles/ResultPage.css";
import CarCard from "./CarCard";

function ResultsPage({
  bestCar,
  remainingCars,
  loading,
  searched,
  error,
  recommendations,
  compareList,
  toggleCompare,
  openExploreModal,
  setCurrentView,
  setShowCompare,
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
            compareList={compareList}
            onToggleCompare={toggleCompare}
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
                compareList={compareList}
                onToggleCompare={toggleCompare}
                onExplore={openExploreModal}
              />
            ))}
          </div>
        </div>
      )}

      {compareList.length === 2 && (
        <div className="compare-bar">
          <p>2 cars selected for comparison</p>
          <button onClick={() => setShowCompare(true)}>
            Compare Now
          </button>
        </div>
      )}

    </div>
  );
}

export default ResultsPage;