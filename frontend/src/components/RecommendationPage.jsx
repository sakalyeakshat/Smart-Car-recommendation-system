import React from "react";
import "../styles/RecommendationPage.css";

function RecommendationPage({
  preferences,
  handleChange,
  handleSubmit,
  loading,
  searched,
  error,
  fuelTypeChoices,
  transmissionChoices,
  bodyTypeChoices,
  resetForm,
  bestCar,
  remainingCars,
  recommendations,
  compareList,
  toggleCompare,
  openExploreModal,
  setShowCompare,
}) {
  return (
    <>
      <div className="layout" id="home">

        <form className="preference-form" onSubmit={handleSubmit}>

          <h2>Vehicle Preferences</h2>

          <div className="field-group">
            <label>Budget (₹ Lakh)</label>
            <input
              type="number"
              name="budget"
              placeholder="Ex. 12"
              min="1"
              max="100"
              step="0.5"
              value={preferences.budget}
              onChange={handleChange}
              required
            />
          </div>

          <div className="field-group">
            <label>Fuel Type</label>
            <select
              name="fuel_type"
              value={preferences.fuel_type}
              onChange={handleChange}
            >
              {fuelTypeChoices.map((opt) => (
                <option key={opt}>{opt}</option>
              ))}
            </select>
          </div>

          <div className="field-group">
            <label>Transmission</label>
            <select
              name="transmission"
              value={preferences.transmission}
              onChange={handleChange}
            >
              {transmissionChoices.map((opt) => (
                <option key={opt}>{opt}</option>
              ))}
            </select>
          </div>

          <div className="field-group">
            <label>Body Type</label>
            <select
              name="body_type"
              value={preferences.body_type}
              onChange={handleChange}
            >
              {bodyTypeChoices.map((opt) => (
                <option key={opt}>{opt}</option>
              ))}
            </select>
          </div>

          <div className="field-group">
            <label>Seating Capacity</label>
            <input
              type="number"
              name="seating"
              min="2"
              max="9"
              value={preferences.seating}
              onChange={handleChange}
            />
          </div>

          <div className="field-group">
            <label>Minimum Mileage</label>
            <input
              type="number"
              name="min_mileage"
              min="5"
              max="40"
              step="0.5"
              value={preferences.min_mileage}
              onChange={handleChange}
            />
          </div>

          <div className="field-group">
            <label>Minimum Safety Rating</label>
            <input
              type="number"
              name="min_safety"
              min="0"
              max="5"
              value={preferences.min_safety}
              onChange={handleChange}
            />
          </div>

          <div className="button-group">
            <button
              type="submit"
              className="submit-button"
              disabled={loading}
            >
              {loading ? "Finding Perfect Cars..." : "Find Best Matches"}
            </button>

            <button
              type="button"
              className="reset-button"
              onClick={resetForm}
            >
              Reset
            </button>
          </div>

        </form>

        <section className="results-panel">
          <div className="empty-state">
            <h2>Welcome To Our System</h2>
            <p>Discover the most suitable vehicle based on your budget.</p>
            <div className="feature-grid">
              <div className="feature-box">
                <h3>Vehicle Suggestions</h3>
                <p>Get cars that best fit your selected criteria.</p>
              </div>
              <div className="feature-box">
                <h3>Budget Friendly</h3>
                <p>Discover vehicles that match your budget without compromising on quality.</p>
              </div>
              <div className="feature-box">
                <h3>Easy Comparisions</h3>
                <p>Compare your favorite cars before making a decision.</p>
              </div>
              <div className="feature-box">
                <h3>150+ Cars Available</h3>
                <p>SUVs, Sedans, Hatchbacks, EVs and more across multiple price ranges.</p>
              </div>
              <div className="feature-box">
                <h3>Top Brands</h3>
                <p>Maruti • Tata • Hyundai • Mahindra • Honda • Toyota</p>
              </div>
              <div className="feature-box">
                <h3>Car Details</h3>
                <p>View specifications, pricing and safety information.</p>
              </div>
            </div>
          </div>
        </section>

        {compareList.length === 2 && (
          <div className="compare-bar">
            <span>{compareList.length} cars selected</span>
            <button onClick={() => setShowCompare(true)}>Compare Now</button>
          </div>
        )}

      </div>
    </>
  );
}

export default RecommendationPage;