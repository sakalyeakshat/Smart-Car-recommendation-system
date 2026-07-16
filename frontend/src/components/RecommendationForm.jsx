/**
 * @file RecommendationForm.jsx
 * @description The main user-input form component for the Smart Car Recommendation System.
 * It renders a hero banner and a structured preference form where users can specify:
 * - Budget (in ₹ Lakh)
 * - Fuel type (Petrol, Diesel, CNG, Electric — multi-select checkboxes)
 * - Transmission type (Manual, Automatic — multi-select checkboxes)
 * - Body type (SUV, Sedan, Hatchback, MPV, Van — dropdown)
 * - Seating capacity
 * - Minimum mileage in kmpl (shown only for non-electric fuel types)
 * - Minimum range in km (shown only when Electric is selected)
 * - Minimum safety rating (0–5)
 * Inline validation errors are displayed per field. On submission the form calls
 * the `handleSubmit` callback received from the parent App component.
 */
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
  validationErrors = {},
}) {
  const isElectricSelected = preferences.fuel_type.includes("Electric");
  const hasNonElectricSelected = preferences.fuel_type.some(opt => opt !== "Electric");

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

          <div className={validationErrors.budget ? "field-group has-error" : "field-group"}>
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
            {validationErrors.budget && (
              <span className="field-error-message">{validationErrors.budget}</span>
            )}
          </div>

          <div className={validationErrors.fuel_type ? "field-group checkbox-field-group has-error" : "field-group checkbox-field-group"}>
            <label>Fuel Type</label>
            <div className="checkbox-options-grid">
              {fuelTypeChoices.map((opt) => (
                <label key={opt} className="checkbox-option-label">
                  <input
                    type="checkbox"
                    name="fuel_type"
                    value={opt}
                    checked={preferences.fuel_type.includes(opt)}
                    onChange={handleChange}
                  />
                  <span>{opt}</span>
                </label>
              ))}
            </div>
            {validationErrors.fuel_type && (
              <span className="field-error-message">{validationErrors.fuel_type}</span>
            )}
          </div>

          <div className={validationErrors.transmission ? "field-group checkbox-field-group has-error" : "field-group checkbox-field-group"}>
            <label>Transmission</label>
            <div className="checkbox-options-grid">
              {transmissionChoices.map((opt) => (
                <label key={opt} className="checkbox-option-label">
                  <input
                    type="checkbox"
                    name="transmission"
                    value={opt}
                    checked={preferences.transmission.includes(opt)}
                    onChange={handleChange}
                  />
                  <span>{opt}</span>
                </label>
              ))}
            </div>
            {validationErrors.transmission && (
              <span className="field-error-message">{validationErrors.transmission}</span>
            )}
          </div>

          <div className={validationErrors.body_type ? "field-group has-error" : "field-group"}>
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
            {validationErrors.body_type && (
              <span className="field-error-message">{validationErrors.body_type}</span>
            )}
          </div>

          <div className={validationErrors.seating ? "field-group has-error" : "field-group"}>
            <label>Seating Capacity</label>
            <input
              type="number"
              name="seating"
              min="2"
              max="9"
              value={preferences.seating}
              onChange={handleChange}
              required
            />
            {validationErrors.seating && (
              <span className="field-error-message">{validationErrors.seating}</span>
            )}
          </div>

          {(!isElectricSelected || hasNonElectricSelected) && (
            <div className={validationErrors.min_mileage ? "field-group has-error" : "field-group"}>
              <label>Minimum Mileage (kmpl)</label>
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
              {validationErrors.min_mileage && (
                <span className="field-error-message">{validationErrors.min_mileage}</span>
              )}
            </div>
          )}

          {isElectricSelected && (
            <div className={validationErrors.min_range ? "field-group has-error" : "field-group"}>
              <label>Minimum Range (km)</label>
              <input
                type="number"
                name="min_range"
                placeholder="Ex. 300"
                min="100"
                max="800"
                step="10"
                value={preferences.min_range}
                onChange={handleChange}
                required
              />
              {validationErrors.min_range && (
                <span className="field-error-message">{validationErrors.min_range}</span>
              )}
            </div>
          )}

          <div className={validationErrors.min_safety ? "field-group has-error" : "field-group"}>
            <label>Minimum Safety Rating</label>
            <input
              type="number"
              name="min_safety"
              min="0"
              max="5"
              value={preferences.min_safety}
              onChange={handleChange}
              required
            />
            {validationErrors.min_safety && (
              <span className="field-error-message">{validationErrors.min_safety}</span>
            )}
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