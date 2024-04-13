import SearchBar from "../../components/searchbar/SearchBar.jsx";
import "./home.scss";

export default function Home() {
  return (
    <div className="home">
      <div className="text-container">
        <section className="wrapper">
          <h1 className="title">Find Real Estate & Get Your Dream Place</h1>
          <p className="description">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Nemo
            repellendus praesentium reiciendis asperiores nesciunt eius.
            Reprehenderit possimus eos ea, incidunt vitae, aperiam corporis
            facere beatae repudiandae, numquam eius id sapiente.
          </p>
          <SearchBar />
          <div className="statistics-section">
            <div className="statistic-item">
              <h1>7+</h1>
              <h2>Years of Experience</h2>
            </div>
            <div className="statistic-item">
              <h1>172</h1>
              <h2>Awards Gained</h2>
            </div>
            <div className="statistic-item">
              <h1>1700+</h1>
              <h2>Properties Ready</h2>
            </div>
          </div>
        </section>
      </div>
      <div className="image-container">
        <img src="bg.png" alt="" />
      </div>
    </div>
  );
}
