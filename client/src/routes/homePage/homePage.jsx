import SearchBar from "../../components/searchBar/SearchBar";
import "./homePage.scss";

function HomePage() {
  return (
    <div className="homePage">
      <div className="bgDecor" aria-hidden="true">
        <div className="orb orbGold" />
        <div className="orb orbBlue" />
        <div className="gridOverlay" />
      </div>

      <div className="hero">
        <h1 className="title">
          Find Real Estate &<br />
          Get Your Dream Place
        </h1>
        <p className="subtitle">
          Discover thousands of properties for sale and rent in the best
          locations. Smart filters, interactive maps, and direct owner
          messaging — all in one place.
        </p>
        <SearchBar />
        <div className="boxes">
          <div className="box">
            <h1>16+</h1>
            <h2>Years of Experience</h2>
          </div>
          <div className="box">
            <h1>200</h1>
            <h2>Awards Gained</h2>
          </div>
          <div className="box">
            <h1>2000+</h1>
            <h2>Properties Ready</h2>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
