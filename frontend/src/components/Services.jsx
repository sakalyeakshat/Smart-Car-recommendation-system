import "../styles/Services.css";

function Services() {
  return (
    <section className="services-page">
      <div className="services-container">

        <span className="services-tag">What Goes Into a Match</span>
        <h2>Seven Things I Ask, Before Recommending Anything</h2>
        <p className="services-description">
          None of these run in isolation — every car gets weighed against
          all of them together, which is what actually separates a decent
          match from a random one.
        </p>

        <div className="services-grid">

          <div className="service-card">
            <div className="service-icon">💰</div>
            <h3>Your Actual Budget</h3>
            <p>
              Not a rough estimate — I check if a car's real price range
              genuinely fits what you said you'd spend.
            </p>
          </div>

          <div className="service-card">
            <div className="service-icon">⛽</div>
            <h3>Fuel You'd Actually Drive</h3>
            <p>
              Petrol, Diesel, CNG, or Electric — whatever runs your
              daily commute, not what's trending.
            </p>
          </div>

          <div className="service-card">
            <div className="service-icon">⚙️</div>
            <h3>How You Like to Drive</h3>
            <p>
              Manual if you enjoy the control, Automatic if you'd
              rather not think about it in traffic.
            </p>
          </div>

          <div className="service-card">
            <div className="service-icon">🛡️</div>
            <h3>Safety, Weighted In</h3>
            <p>
              This isn't a footnote on the spec sheet — a car's safety
              rating directly pulls its match score up or down.
            </p>
          </div>

          <div className="service-card">
            <div className="service-icon">👨‍👩‍👧</div>
            <h3>Who's Actually Riding With You</h3>
            <p>
              Solo commutes and family road trips need very different
              cars — seating capacity is part of the math.
            </p>
          </div>

          <div className="service-card">
            <div className="service-icon">🚗</div>
            <h3>The Shape That Fits Your Life</h3>
            <p>
              SUV, Sedan, Hatchback, MPV, Van, or Pickup — I don't
              assume, I ask.
            </p>
          </div>

        </div>

      </div>

      <svg className="services-bg-car car-a" viewBox="0 0 500 200">
        <path
          d="M80 130 L150 80 L330 80 L390 120 L450 120 L450 150 L80 150 Z"
          fill="none" stroke="#32d3ff" strokeWidth="4"
        />
        <circle cx="150" cy="150" r="20" fill="none" stroke="#32d3ff" strokeWidth="4" />
        <circle cx="360" cy="150" r="20" fill="none" stroke="#32d3ff" strokeWidth="4" />
      </svg>

    </section>
  );
}

export default Services;
