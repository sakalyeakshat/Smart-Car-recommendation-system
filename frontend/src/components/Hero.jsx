import React from "react";
import "../styles/Hero.css";

function Hero() {
  return (
    <header className="hero">
      <div className="hero-content">
        <span className="tagline">
          DRIVE MATCH AI
        </span>

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
  );
}

export default Hero;