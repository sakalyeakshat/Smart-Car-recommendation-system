import Hero from "./components/Hero";
import { useState, useEffect } from "react";
import RecommendationPage from "./components/RecommendationPage";
import ResultsPage from "./components/ResultsPage";
import CompareModal from "./components/CompareModal";
import ExploreModal from "./components/ExploreModal";

import "./App.css";

const BACKEND_URL = "http://localhost:8000/recommend";

const fuelOptions = [
  "Petrol",
  "Diesel",
  "CNG",
  "Electric",
];

const transmissionOptions = [
  "Manual",
  "Automatic",
];

const bodyOptions = [
  "SUV",
  "Sedan",
  "Hatchback",
  "MPV",
  "Van",
  "Pickup",
];

function App() {
  const [preferences, setPreferences] = useState({
    budget: "",
    fuel_type: "Petrol",
    transmission: "Manual",
    body_type: "SUV",
    seating: 5,
    min_mileage: "",
    min_safety: 3,
  });

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");
  const [currentView, setCurrentView] = useState("home");
  const [compareList, setCompareList] = useState([]);
  const [showCompare, setShowCompare] = useState(false);
  const [selectedCar, setSelectedCar] = useState(null);
  const [showExplore, setShowExplore] = useState(false);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [currentView]);

  function handleChange(e) {
    const { name, value } = e.target;
    setPreferences((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  function resetForm() {
    setPreferences({
      budget: "",
      fuel_type: "Petrol",
      transmission: "Manual",
      body_type: "SUV",
      seating: 5,
      min_mileage: "",
      min_safety: 3,
    });
    setRecommendations([]);
    setError("");
    setSearched(false);
  }

  function toggleCompare(car) {
    setCompareList((prev) => {
      const alreadySelected = prev.find(
        (c) => c.brand === car.brand && c.model === car.model
      );

      if (alreadySelected) {
        return prev.filter(
          (c) => !(c.brand === car.brand && c.model === car.model)
        );
      }

      if (prev.length >= 2) {
        alert("You can only compare 2 cars at a time. Remove one first.");
        return prev;
      }

      return [...prev, car];
    });
  }

  function clearCompare() {
    setCompareList([]);
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
      const response = await fetch(BACKEND_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
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

      if (!response.ok) {
        throw new Error();
      }

      const data = await response.json();
      setRecommendations(data.recommendations || []);
      setCurrentView("results");

    } catch {
      setRecommendations([]);
      setError(
        "Unable to connect with backend. Please ensure FastAPI server is running."
      );
    } finally {
      setLoading(false);
    }
  }

  const bestCar = recommendations.length > 0 ? recommendations[0] : null;
  const remainingCars = recommendations.slice(1);

  return (
    <div className="page">
      {showExplore && (
        <ExploreModal
          car={selectedCar}
          onClose={() => setShowExplore(false)}
        />
      )}
      <nav className="navbar">
        <span className="navbar-logo">Smart Car Recommendation System</span>
      </nav>

      <div className="background-glow glow1"></div>
      <div className="background-glow glow2"></div>

      <svg className="bg-car car-one" viewBox="0 0 500 200">
        <path
          d="M80 130 L150 80 L330 80 L390 120 L450 120 L450 150 L80 150 Z"
          fill="none"
          stroke="#32d3ff"
          strokeWidth="4"
        />
        <circle
          cx="150"
          cy="150"
          r="20"
          fill="none"
          stroke="#32d3ff"
          strokeWidth="4"
        />
        <circle
          cx="360"
          cy="150"
          r="20"
          fill="none"
          stroke="#32d3ff"
          strokeWidth="4"
        />
      </svg>

      <svg className="bg-car car-two" viewBox="0 0 500 200">
        <path
          d="M100 130 L170 90 L310 90 L370 120 L430 120 L430 150 L100 150 Z"
          fill="none"
          stroke="#9b5cff"
          strokeWidth="4"
        />
        <circle
          cx="170"
          cy="150"
          r="18"
          fill="none"
          stroke="#9b5cff"
          strokeWidth="4"
        />
        <circle
          cx="350"
          cy="150"
          r="18"
          fill="none"
          stroke="#9b5cff"
          strokeWidth="4"
        />
      </svg>

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
                searched={searched}
                error={error}
                recommendations={recommendations}
                bestCar={bestCar}
                remainingCars={remainingCars}
                compareList={compareList}
                toggleCompare={toggleCompare}
                openExploreModal={openExploreModal}
                setShowCompare={setShowCompare}
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
            compareList={compareList}
            toggleCompare={toggleCompare}
            openExploreModal={openExploreModal}
            setShowCompare={setShowCompare}
            setCurrentView={setCurrentView}
          />
        )}

        <footer className="footer">
          <p>DriveMatch AI • Smart Vehicle Recommendation System</p>
        </footer>

        {showCompare && (
          <CompareModal
            cars={compareList}
            onClose={() => {
              setShowCompare(false);
              clearCompare();
            }}
          />
        )}
      </>

    </div>
  );
}

export default App;