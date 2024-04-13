import "./layout.scss";

import Navbar from "./components/navbar/Navbar.jsx";
import Home from "./routes/home/Home.jsx";

function App() {
  return (
    <>
      <div className="layout">
        <div className="navbar">
          <Navbar />
        </div>
        <div className="content">
          <Home />
        </div>
      </div>
    </>
  );
}

export default App;
