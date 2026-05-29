/**
 * Header Component
 * Displays the application title and description
 */

export function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="header-title">SWS AI Policy Assistant</h1>
        <p className="header-subtitle">
          Ask questions from internal company documents instantly.
        </p>
      </div>
    </header>
  );
}

export default Header;
