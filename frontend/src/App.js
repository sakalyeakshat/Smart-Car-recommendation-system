import Hero from "./components/Hero";
import { useState, useEffect } from "react";
import RecommendationPage from "./components/RecommendationPage";
import ResultsPage from "./components/ResultsPage";
import ExploreModal from "./components/ExploreModal";

import "./App.css";

const fuelOptions = ["Petrol", "Diesel", "CNG", "Electric"];
const transmissionOptions = ["Manual", "Automatic"];
const bodyOptions = ["SUV", "Sedan", "Hatchback", "MPV", "Van", "Pickup"];

function App() {
  const [preferences, setPreferences] = useState({
    budget: "",
    fuel_type: "",
    transmission: "",
    body_type: "",
    seating: 5,
    min_mileage: "",
    min_safety: 3,
  });

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");
  const [currentView, setCurrentView] = useState("home");
  const [selectedCar, setSelectedCar] = useState(null);
  const [showExplore, setShowExplore] = useState(false);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [currentView]);

  // pressing the browser back button returns to the home view
  useEffect(() => {
    function handlePopState() {
      setCurrentView("home");
    }
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  function handleChange(e) {
    const { name, value } = e.target;
    setPreferences((prev) => ({ ...prev, [name]: value }));
  }

  function resetForm() {
    setPreferences({
      budget: "",
      fuel_type: "",
      transmission: "",
      body_type: "",
      seating: 5,
      min_mileage: "",
      min_safety: 3,
    });
    setRecommendations([]);
    setError("");
    setSearched(false);
  }

  function openExploreModal(car) {
    setSelectedCar(car);
    setShowExplore(true);
  }

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
        <span className="navbar-logo">Smart Car Recommendation System</span>
      </nav>

      <>
        {currentView === "home" && (
          <>
            <Hero />
            <section id="recommendation-form">
              <RecommendationPage
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