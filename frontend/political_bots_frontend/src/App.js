import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [health, setHealth] = useState(false)

  useEffect(() => {
    fetch("http://localhost:8000/health").then(res => res.json()).then(data => {
      setHealth(data.health);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edits <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>Health status: {health}.</p>
      </header>
    </div>
  );
}

export default App;
