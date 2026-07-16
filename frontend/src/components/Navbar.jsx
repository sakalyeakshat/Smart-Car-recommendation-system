/**
 * @file Navbar.jsx
 * @description Global navigation bar component for the Smart Car Recommendation System.
 *
 * Renders a persistent top-of-page header (`<nav>`) that contains:
 * - The application logo image (`/logo.png` from the public directory).
 * - The application title "Smart Car Recommendation System" as branded text.
 *
 * This component is stateless and receives no props; it is displayed on every view
 * of the application (both the form view and the results view) as managed by App.jsx.
 */
import "../styles/Navbar.css";

/**
 * Component representing the global navigation header.
  The rendered navigation bar.
 */
function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <img src="/logo.png" className="navbar-logo-img" alt="Car Logo" />
        <span className="navbar-logo">Smart Car Recommendation System</span>
      </div>
    </nav>
  );
}

export default Navbar;
