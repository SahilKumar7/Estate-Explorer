import { useState } from "react";
import "./navbar.scss";

export default function Navbar() {
  const [showMenu, setShowMenu] = useState(false);

  return (
    <nav>
      <div className="left">
        <a href="" className="logo">
          <img src="/logo.png" alt="Estate Explorer Logo" />
          <span>Estate Explorer</span>
        </a>
        <a href="/">Home</a>
        <a href="/">About</a>
        <a href="/">Contact</a>
        <a href="/">Agents</a>
      </div>
      <div className="right">
        <a href="/">Sign In</a>
        <a href="/" className="sign-up">
          Sign Up
        </a>
        <div className="menu-icon">
          <img
            src="menu.png"
            alt="Menu Icon"
            onClick={() => setShowMenu((prev) => !prev)}
          />
        </div>
        <div className={showMenu ? "menu active" : "menu"}>
          <a href="/">Home</a>
          <a href="/">About</a>
          <a href="/">Contact</a>
          <a href="/">Agents</a>
          <a href="/">Sign In</a>
          <a href="/" className="sign-up">
            Sign Up
          </a>
        </div>
      </div>
    </nav>
  );
}
