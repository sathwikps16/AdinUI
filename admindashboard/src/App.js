import React from 'react';
import './styles.css';
import Header from './components/Header';
import Nav from './components/Nav';
import Main from './components/Main';
import KnowledgeBase from './components/KnowledgeBase';
import TicketSystem from './components/TicketSystem'
// import TicketChoose from './components/TicketChoose';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { MyContextProvider } from './components/MyContext';  
import TicketChoose from './components/TicketChoose';

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
              {/* <Route path="/ticket-choose" element={<TicketChoose />} /> */}
              <Route path="/ticket-system" element={<TicketSystem />} />
            </Routes>
          </div>
        </div>
      </Router>
    </MyContextProvider>  
  );
}

export default App;
