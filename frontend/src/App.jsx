import { useState, useEffect } from "react";
import RecommendationForm from "./components/RecommendationForm";
import ResultsPage from "./components/ResultsPage";
import ExploreModal from "./components/ExploreModal";

import "./App.css";

const fuelOptions = ["Petrol", "Diesel", "CNG", "Electric"];
const transmissionOptions = ["Manual", "Automatic"];
const bodyOptions = ["SUV", "Sedan", "Hatchback", "MPV", "Van", "Pickup"];

const defaultPrefs = {
  budget: "",
  fuel_type: "",
  transmission: "",
  body_type: "",
  seating: 5,
  min_mileage: "",
  min_safety: 3,
};

/**
 * Main application component managing preferences, recommendations, and current view state.
 * The rendered application layout.
 */
function App() {
  const [preferences, setPreferences] = useState(defaultPrefs);

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");
  const [currentView, setCurrentView] = useState("home");
  const [selectedCar, setSelectedCar] = useState(null);
  const [showExplore, setShowExplore] = useState(false);

  /**
   * Scroll to top of the page when the view changes.
   */
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [currentView]);

  /**
   * Listen for browser back button to navigate back to the home view.
   */
  useEffect(() => {
    function handlePopState() {
      setCurrentView("home");
    }
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  /**
   * Update preference values dynamically on input change.
   * @param {React.ChangeEvent<HTMLInputElement|HTMLSelectElement>} e - Change event object.
   */
  function handleChange(e) {
    const { name, value } = e.target;
    setPreferences((prev) => ({ ...prev, [name]: value }));
  }

  /**
   * Reset the preference form and results state.
   */
  function resetForm() {
    setPreferences(defaultPrefs);
    setRecommendations([]);
    setError("");
    setSearched(false);
  }

  /**
   * Opens the explore modal for a specific car.
   * - Selected car object.
   */
  function openExploreModal(car) {
    setSelectedCar(car);
    setShowExplore(true);
  }

  /**
   * Handle form submission, fetch recommendations from API, and switch views.
   *  e - Form submission event.
   */
  async function handleSubmit(e) {
    e.preventDefault();

    setLoading(true);
    setError("");
    setSearched(true);

    try {
      const response = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          budget: Number(preferences.budget),
          fuel_type: preferences.fuel_type,
          transmission: preferences.transmission,
          body_type: preferences.body_type,
          seating: Number(preferences.seating),
          min_mileage: Number(preferences.min_mileage),
          min_safety: Number(preferences.min_safety),
        }),
      });

      if (!response.ok) throw new Error();

      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch {
      setRecommendations([]);
      setError("Unable to connect with backend. Please ensure FastAPI server is running.");
    } finally {
      setLoading(false);
      
      /** update URL so back button works properly */
      window.history.pushState({ view: "results" }, "", window.location.href);
      setCurrentView("results");
    }
  }

  const bestCar = recommendations.length > 0 ? recommendations[0] : null;
  const remainingCars = recommendations.slice(1);

  return (
    <div className="page">
      {showExplore && (
        <ExploreModal car={selectedCar} onClose={() => setShowExplore(false)} />
      )}

      <nav className="navbar">
        <div className="navbar-brand">
          <svg className="navbar-logo-img" viewBox="0 0 100 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M 12 25 c 0 -3.3 2.7 -6 6 -6 s 6 2.7 6 6" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
            <path d="M 72 25 c 0 -3.3 2.7 -6 6 -6 s 6 2.7 6 6" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
            <path d="M 5 25 h 7 M 30 25 h 42 M 84 25 h 11" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
            <path d="M 6 25 Q 12 18 20 18 Q 30 18 42 13 Q 56 9 70 13 Q 84 17 91 21 Q 94 23 94 25" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
            <path d="M 33 17.5 Q 46 14 58 14 Q 70 14 78 17.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
          <span className="navbar-logo">Smart Car Recommendation System</span>
        </div>
      </nav>

      <>
        {currentView === "home" && (
          <>
            <section id="recommendation-form">
              <RecommendationForm
                preferences={preferences}
                handleChange={handleChange}
                handleSubmit={handleSubmit}
                loading={loading}
                resetForm={resetForm}
                fuelTypeChoices={fuelOptions}
                transmissionChoices={transmissionOptions}
                bodyTypeChoices={bodyOptions}
              />
            </section>
          </>
        )}

        {currentView === "results" && (
          <ResultsPage
            bestCar={bestCar}
            remainingCars={remainingCars}
            loading={loading}
            searched={searched}
            error={error}
            recommendations={recommendations}
            openExploreModal={openExploreModal}
            setCurrentView={setCurrentView}
          />
        )}

        <footer className="footer">
          <p>DriveMatch AI • Smart Vehicle Recommendation System</p>
        </footer>
      </>
    </div>
  );
}

export default App;