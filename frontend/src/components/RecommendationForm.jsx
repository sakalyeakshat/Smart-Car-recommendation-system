import "../styles/RecommendationForm.css";

function RecommendationForm({
  preferences,
  handleChange,
  handleSubmit,
  loading,
  fuelTypeChoices,
  transmissionChoices,
  bodyTypeChoices,
  resetForm,
}) {
  return (
    <>
      <header className="hero">
        <div className="hero-content">
          <h1>
            Find Your Perfect Car
            <br />
            Instantly
          </h1>
          <p>
            Get matched with cars that fit your budget, your lifestyle, and your priorities.
          </p>
        </div>
      </header>

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
              required
            >
              <option value="">Select Fuel Type</option>
              {fuelTypeChoices.map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>

          <div className="field-group">
            <label>Transmission</label>
            <select
              name="transmission"
              value={preferences.transmission}
              onChange={handleChange}
              required
            >
              <option value="">Select Transmission</option>
              {transmissionChoices.map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>

          <div className="field-group">
            <label>Body Type</label>
            <select
              name="body_type"
              value={preferences.body_type}
              onChange={handleChange}
              required
            >
              <option value="">Select Body Type</option>
              {bodyTypeChoices.map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
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
              placeholder="Ex. 15"
              min="5"
              max="30"
              step="0.5"
              value={preferences.min_mileage}
              onChange={handleChange}
              required
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


      </div>
    </>
  );
}

export default RecommendationForm;