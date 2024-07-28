import "./aboutPage.scss";

function AboutPage() {
  return (
    <div className="aboutPage">
      <div className="hero">
        <h1>About Estate Explorer</h1>
        <p>
          Your trusted partner in finding the perfect property. We connect
          buyers, sellers, and renters with premium real estate opportunities.
        </p>
      </div>

      <div className="mission">
        <div className="card">
          <h2>Our Mission</h2>
          <p>
            To simplify the real estate journey by providing a seamless,
            transparent platform where people can discover, list, and connect
            over properties that match their lifestyle and budget.
          </p>
        </div>
        <div className="card">
          <h2>Our Vision</h2>
          <p>
            To become the go-to real estate marketplace that empowers everyone
            -- from first-time renters to seasoned investors -- to make
            confident property decisions backed by rich data and direct
            communication.
          </p>
        </div>
      </div>

      <div className="features">
        <h2>Why Choose Us</h2>
        <div className="grid">
          <div className="featureCard">
            <div className="icon">&#x1F50D;</div>
            <h3>Smart Search</h3>
            <p>
              Filter by city, price, bedrooms, property type, and more to find
              exactly what you need.
            </p>
          </div>
          <div className="featureCard">
            <div className="icon">&#x1F4AC;</div>
            <h3>Direct Messaging</h3>
            <p>
              Chat directly with property owners in real-time -- no middlemen,
              no delays.
            </p>
          </div>
          <div className="featureCard">
            <div className="icon">&#x1F5FA;</div>
            <h3>Interactive Maps</h3>
            <p>
              Explore properties on a map with nearby schools, transit, and
              restaurants at a glance.
            </p>
          </div>
          <div className="featureCard">
            <div className="icon">&#x1F4BE;</div>
            <h3>Save & Compare</h3>
            <p>
              Bookmark your favorite listings and revisit them anytime from your
              profile dashboard.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AboutPage;
