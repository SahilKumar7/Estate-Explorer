import { useState } from "react";
import "./contactPage.scss";

function ContactPage() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    e.target.reset();
    setTimeout(() => setSubmitted(false), 4000);
  };

  return (
    <div className="contactPage">
      <div className="formSide">
        <h1>Get in Touch</h1>
        <p>
          Have a question or want to work with us? Fill out the form and we will
          get back to you within 24 hours.
        </p>
        <form onSubmit={handleSubmit}>
          <div className="item">
            <label htmlFor="name">Full Name</label>
            <input
              id="name"
              name="name"
              type="text"
              placeholder="John Doe"
              required
            />
          </div>
          <div className="item">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="john@example.com"
              required
            />
          </div>
          <div className="item">
            <label htmlFor="message">Message</label>
            <textarea
              id="message"
              name="message"
              placeholder="How can we help you?"
              rows={5}
              required
            />
          </div>
          <button type="submit">Send Message</button>
          {submitted && (
            <span className="success">Message sent successfully!</span>
          )}
        </form>
      </div>
      <div className="infoSide">
        <div className="infoCard">
          <h3>Office Address</h3>
          <p>123 Real Estate Blvd, Suite 400</p>
          <p>New York, NY 10001</p>
        </div>
        <div className="infoCard">
          <h3>Email Us</h3>
          <p>hello@estateexplorer.com</p>
          <p>support@estateexplorer.com</p>
        </div>
        <div className="infoCard">
          <h3>Call Us</h3>
          <p>+1 (555) 123-4567</p>
          <p>Mon - Fri, 9am - 6pm EST</p>
        </div>
      </div>
    </div>
  );
}

export default ContactPage;
