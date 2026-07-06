import { useState, useEffect } from "react";
import "../styles/ExploreModal.css";

function ExploreModal({ car, onClose }) {
  const [keyStrengths, setKeyStrengths] = useState([]);
  const [thingsToConsider, setThingsToConsider] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!car) return;

    setLoading(true);
    setError(null);

    fetch("/explore", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        fuel_type: car.fuel_type,
        transmission: car.transmission,
        body_type: car.body_type,
      }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch explore data");
        return res.json();
      })
      .then((data) => {
        setKeyStrengths(data.key_strengths);
        setThingsToConsider(data.things_to_consider);
        setLoading(false);
      })
      .catch(() => {
        setError("Could not load details. Please try again.");
        setLoading(false);
      });
  }, [car]);

  if (!car) return null;

  return (
    <div className="modal-overlay">
      <div className="explore-modal">

        <button className="modal-close" onClick={onClose}>×</button>

        <h2>Why This Car Stands Out</h2>

        {loading && (
          <div className="explore-loading">
            <div className="explore-spinner"></div>
            <p>Loading details...</p>
          </div>
        )}

        {error && <div className="explore-error">{error}</div>}

        {!loading && !error && (
          <>
            <div className="explore-section">
              <h3>Key Strengths</h3>
              <ul>
                {keyStrengths.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="explore-section">
              <h3>Things to Consider</h3>
              <ul>
                {thingsToConsider.map((item, index) => (
                  <li key={index}>⚠ {item}</li>
                ))}
              </ul>
            </div>
          </>
        )}

      </div>
    </div>
  );
}

export default ExploreModal;
