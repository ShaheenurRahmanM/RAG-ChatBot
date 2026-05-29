/**
 * Loader Component
 * Displays loading indicator during API calls
 */

export function Loader() {
  return (
    <div className="loader-container">
      <div className="loader">
        <div className="loader-dot"></div>
        <div className="loader-dot"></div>
        <div className="loader-dot"></div>
      </div>
      <p className="loader-text">Thinking...</p>
    </div>
  );
}

export default Loader;
