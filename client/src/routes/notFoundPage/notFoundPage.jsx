import { Link } from "react-router-dom";
import "./notFoundPage.scss";

function NotFoundPage() {
  return (
    <div className="notFoundPage">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The page you are looking for does not exist or has been moved.</p>
      <Link to="/" className="homeLink">
        Back to Home
      </Link>
    </div>
  );
}

export default NotFoundPage;
