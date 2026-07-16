/**
 * App.jsx
 *  Root application component for the Smart Car Recommendation System.
 * Responsibilities:
 * - Manages global application state (user preferences, recommendations, loading,
 *   errors, validation errors, current view, selected car, and explore modal).
 * - Defines the available option lists for fuel type, transm
 * Child components rendered by this file:
 * - `<Navbar>`            — Persistent top navigation bar.
 * - `<RecommendationForm>` — Preference input form (shown in "home" view).
 * - `<ResultsPage>`        — Recommendation results display (shown in "results" view).
 * - `<ExploreModal>`       — Car detail modal overlay (shown on demand).
 * - `<Footer>`             — Persistent bottom footer.
 */
import { useState, useEffect } from "react";
import RecommendationForm from "./components/RecommendationForm";
import ResultsPage from "./components/ResultsPage";
import ExploreModal from "./components/ExploreModal";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import "./App.css";

const fuelOptions = ["Petrol", "Diesel", "CNG", "Electric"];
const transmissionOptions = ["Manual", "Automatic"];
const bodyOptions = ["SUV", "Sedan", "Hatchback", "MPV", "Van"];

const defaultPrefs = {
  budget: "",
  fuel_type: [],
  transmission: [],
  body_type: "",
  seating: 5,
  min_mileage: "",
  min_safety: 3,
  min_range: "",
};

/**
 * Top-level React component that wires together all views and shared state.
 * @returns {JSX.Element} The full application layout.
 */
function App() {
  const [preferences, setPreferences] = useState(defaultPrefs);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");
  const [validationErrors, setValidationErrors] = useState({});
  const [currentView, setCurrentView] = useState("home");
  const [selectedCar, setSelectedCar] = useState(null);
  const [showExplore, setShowExplore] = useState(false);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [currentView]);

  useEffect(() => {
    function handlePopState() {
      setCurrentView("home");
    }
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setValidationErrors((prev) => ({ ...prev, [name]: "" }));

    if (type === "checkbox") {
      setPreferences((prev) => {
        const currentList = prev[name] || [];
        if (checked) {
          return { ...prev, [name]: [...currentList, value] };
        } else {
          return { ...prev, [name]: currentList.filter((item) => item !== value) };
        }
      });
    } else {
      setPreferences((prev) => ({ ...prev, [name]: value }));
    }
  }

  function resetForm() {
    setPreferences(defaultPrefs);
    setRecommendations([]);
    setError("");
    setValidationErrors({});
    setSearched(false);
  }

  function openExploreModal(car) {
    setSelectedCar(car);
    setShowExplore(true);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setValidationErrors({});

    const errors = {};
    if (!preferences.budget || Number(preferences.budget) <= 0) {
      errors.budget = "Please enter a budget greater than 0.";
    }
    if (!preferences.fuel_type || preferences.fuel_type.length === 0) {
      errors.fuel_type = "Please select at least one Fuel Type.";
    }
    if (!preferences.transmission || preferences.transmission.length === 0) {
      errors.transmission = "Please select at least one Transmission Type.";
    }
    if (!preferences.body_type) {
      errors.body_type = "Please select a Body Type.";
    }
    if (!preferences.seating || Number(preferences.seating) < 2 || Number(preferences.seating) > 9) {
      errors.seating = "Please enter seating capacity between 2 and 9.";
    }

    const isElectric = preferences.fuel_type.includes("Electric");
    const hasNonElectric = preferences.fuel_type.some(opt => opt !== "Electric");

    if (!isElectric || hasNonElectric) {
      if (!preferences.min_mileage || Number(preferences.min_mileage) < 5 || Number(preferences.min_mileage) > 30) {
        errors.min_mileage = "Please enter minimum mileage between 5 and 30 kmpl.";
      }
    }

    if (isElectric) {
      if (!preferences.min_range || Number(preferences.min_range) < 100 || Number(preferences.min_range) > 800) {
        errors.min_range = "Please enter minimum range between 100 and 800 km.";
      }
    }

    if (preferences.min_safety === "" || preferences.min_safety === undefined || Number(preferences.min_safety) < 0 || Number(preferences.min_safety) > 5) {
      errors.min_safety = "Please enter minimum safety rating between 0 and 5.";
    }

    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      return;
    }

    setLoading(true);
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
          min_mileage: preferences.fuel_type.includes("Electric") && preferences.fuel_type.length === 1 ? 0 : Number(preferences.min_mileage || 0),
          min_safety: Number(preferences.min_safety),
          min_range: preferences.fuel_type.includes("Electric") ? Number(preferences.min_range || 0) : null,
        }),
      });

      if (!response.ok) {
        if (response.status === 422) {
          throw new Error("Invalid preferences. Please check your inputs.");
        }
        throw new Error("Unable to connect with backend. Please ensure FastAPI server is running.");
      }

      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (err) {
      setRecommendations([]);
      setError(err.message || "Unable to connect with backend.");
    } finally {
      setLoading(false);
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

      <Navbar />

      <>
        {currentView === "home" && (
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
              validationErrors={validationErrors}
            />
          </section>
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

        <Footer />
      </>
    </div>
  );
}

export default App;