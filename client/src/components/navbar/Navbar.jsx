import { useContext, useEffect, useState } from "react";
import "./navbar.scss";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import { useNotificationStore } from "../../lib/notificationStore";
import apiRequest from "../../lib/apiRequest";

function Navbar() {
  const [open, setOpen] = useState(false);
  const { currentUser, updateUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const fetch = useNotificationStore((state) => state.fetch);
  const number = useNotificationStore((state) => state.number);

  useEffect(() => {
    if (currentUser) fetch();
  }, [currentUser, fetch]);

  const handleMobileLogout = async () => {
    try {
      await apiRequest.post("/auth/logout");
      updateUser(null);
      setOpen(false);
      navigate("/");
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <nav>
      <div className="left">
        <Link to="/" className="logo">
          <span className="logoIcon">E</span>
          <span>Estate Explorer</span>
        </Link>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">Contact</Link>
        <Link to="/list">Listings</Link>
      </div>
      <div className="right">
        {currentUser ? (
          <div className="user">
            <img src={currentUser.avatar || "/noavatar.jpg"} alt="" />
            <span>{currentUser.username}</span>
            <Link to="/profile" className="profile">
              {number > 0 && <div className="notification">{number}</div>}
              <span>Profile</span>
            </Link>
          </div>
        ) : (
          <>
            <Link to="/login" className="login">Sign in</Link>
            <Link to="/register" className="register">Sign up</Link>
          </>
        )}
        <div className="menuIcon">
          <img
            src="/menu.png"
            alt=""
            onClick={() => setOpen((prev) => !prev)}
          />
        </div>
        <div className={open ? "menu active" : "menu"}>
          <Link to="/" onClick={() => setOpen(false)}>Home</Link>
          <Link to="/about" onClick={() => setOpen(false)}>About</Link>
          <Link to="/contact" onClick={() => setOpen(false)}>Contact</Link>
          <Link to="/list" onClick={() => setOpen(false)}>Listings</Link>
          {currentUser ? (
            <>
              <Link to="/profile" onClick={() => setOpen(false)}>Profile</Link>
              <span onClick={handleMobileLogout} style={{ cursor: "pointer" }}>
                Logout
              </span>
            </>
          ) : (
            <>
              <Link to="/login" onClick={() => setOpen(false)}>Sign in</Link>
              <Link to="/register" onClick={() => setOpen(false)}>Sign up</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
