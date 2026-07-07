import "../styles/Navbar.css";

/**
 * Component representing the global navigation header.
 * @returns {JSX.Element} The rendered navigation bar.
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
