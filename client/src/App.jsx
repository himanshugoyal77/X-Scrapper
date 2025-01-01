import axios from "axios";
import { useEffect, useState } from "react";

const Home = () => {
  const [data, setData] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    setMessage("Initializing...");
    axios
      .get("http://127.0.0.1:5000/")
      .then(() => {
        setMessage("Intialization successful");
      })
      .catch((error) => {
        console.error("There was an error!", error);
        setMessage("There was an error connecting to the server");
      });
  }, []);

  const handleClick = () => {
    setMessage("Running the script...");
    axios
      .get("http://127.0.0.1:5000/trending")
      .then((response) => {
        setData(response.data);
        setMessage("Script ran successfully");
      })
      .catch((error) => {
        console.error("There was an error!", error);
        setMessage("There was an error running the script");
      });
  };

  return (
    <div className="container">
      <button className="action-button" onClick={handleClick}>
        Click here to run the script
      </button>
      {message && <p className="status-message">{message}</p>}
      {data && (
        <div className="results-container">
          <h2 className="timestamp-header">
            These are the most happening topics as on {data.data.timestamp}
          </h2>

          <ul className="trending-list">
            {data &&
              data.data.trends.slice(0, 5).map((trend, index) => (
                <li className="trending-item" key={index}>
                  {trend}
                </li>
              ))}
          </ul>

          <h2 className="ip-header">
            The IP address used for this query was {data.data.ip_address}
          </h2>
          <p className="json-label">
            Here&apos;s a JSON extract of this record from the mongoDB
          </p>
          <pre className="json-display">
            {data && JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default Home;
