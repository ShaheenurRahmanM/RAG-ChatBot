/**
 * Main App Component
 * Root component for the SWS AI Policy Assistant
 */

import Header from './components/Header';
import ChatBox from './components/ChatBox';
import './App.css';

export function App() {
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <ChatBox />
      </main>
    </div>
  );
}

export default App;
