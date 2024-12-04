import React from 'react';
import { Link } from 'react-router-dom';
import upload from '../img/upload.png';
import home from '../img/dashboard_icon.png';
import ticket from '../img/ticket.png';

const Nav = () => {
    return (
        <div className="navcontainer">
            <nav className="nav">
                <div className="nav-upper-options">
                    {/* Dashboard */}
                    <div className="nav-option option1">
                        <img
                            src={home}
                            className="nav-img"
                            alt="Dashboard"
                        />
                        <Link to="/" style={{ textDecoration: 'none', color: 'black' }}>
                            <h3>Dashboard</h3>
                        </Link>
                    </div>

                    {/* Document Upload */}
                    <div className="nav-option option2">
                        <img
                            src={upload}
                            className="nav-img"
                            alt="Document Upload"
                        />
                        <Link to="/knowledge-base" style={{ textDecoration: 'none', color: 'black' }}>
                            <h3>Knowledge Base</h3>
                        </Link>
                    </div>

                    {/* Ticketing System */}
                    <div className="nav-option option3">
                        <img
                            src={ticket}
                            className="nav-img"
                            alt="Ticketing System"
                        />
                        <Link to="/ticket-system" style={{ textDecoration: 'none', color: 'black' }}>
                            <h3 style={{ margin: 0, cursor: 'pointer' }}>Ticketing System</h3>
                        </Link>
                    </div>
                </div>
            </nav>
        </div>
    );
};

export default Nav;
