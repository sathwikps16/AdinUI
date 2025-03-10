import React from 'react';
import './styles.css';
import Header from './components/Header';
import Nav from './components/Nav';
import Main from './components/Main';
import KnowledgeBase from './components/KnowledgeBase';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { MyContextProvider } from './components/MyContext';  // Import the context provider

function App() {
  return (
    <MyContextProvider> {/* Wrap your app in the context provider */}
      <Router>
        <div>
          <Header />
          <div className="main-container">
            <Nav />
            <Routes>
              <Route path="/" element={<Main />} />
              <Route path="/knowledge-base" element={<KnowledgeBase />} />
            </Routes>
          </div>
        </div>
      </Router>
    </MyContextProvider>  
  );
}

export default App;
