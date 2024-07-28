import { Link } from "react-router-dom";
import "./footer.scss";

function Footer() {
  return (
    <footer className="footer">
      <div className="footerContent">
        <div className="brand">
          <Link to="/" className="logo">
            <span className="logoIcon">E</span>
            <span className="logoText">Estate Explorer</span>
          </Link>
          <p>
            Your trusted partner in finding the perfect property. Buy, sell, and
            rent with confidence.
          </p>
        </div>
        <div className="links">
          <h4>Quick Links</h4>
          <Link to="/">Home</Link>
          <Link to="/about">About</Link>
          <Link to="/list">Listings</Link>
          <Link to="/contact">Contact</Link>
        </div>
        <div className="contact">
          <h4>Contact</h4>
          <p>hello@estateexplorer.com</p>
          <p>+1 (555) 123-4567</p>
          <p>New York, NY 10001</p>
        </div>
      </div>
      <div className="footerBottom">
        <p>&copy; {new Date().getFullYear()} Estate Explorer. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;
