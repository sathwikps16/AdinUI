import React from 'react';
import './styles.css';
import Header from './components/Header';
import Nav from './components/Nav';
import Main from './components/Main';
import KnowledgeBase from './components/KnowledgeBase';
import TicketChoose from './components/TicketChoose'
import ServiceNow from './components/Ticketing System/ServiceNow';
import ZenDesk from'./components/Ticketing System/ZenDesk';
import Jira from './components/Ticketing System/Jira'
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
              <Route path="/ticket-choose" element={<TicketChoose />} />
              <Route path="/ServiceNow" element={<ServiceNow />} />
              <Route path="/ZenDesk" element={<ZenDesk />} />
              <Route path="/Jira" element={<Jira />} />
            </Routes>
          </div>
        </div>
      </Router>
    </MyContextProvider>  
  );
}

export default App;
